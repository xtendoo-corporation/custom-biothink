import base64
import csv
import io
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class PartnerImportWizard(models.TransientModel):
    _name = "biothink.partner.import.wizard"
    _description = "Partner Import Wizard"

    # Campos existentes para importación de plan contable
    plan_csv_file = fields.Binary(string="Archivo CSV de plan contable")
    plan_file_name = fields.Char(string="Nombre del plan contable")

    # Campos existentes para importación de contactos
    contact_csv_file = fields.Binary(string="Archivo CSV de contactos")
    contact_file_name = fields.Char(string="Nombre del archivo")

    # Campos nuevos para importación de asientos contables
    accounting_csv_file = fields.Binary(string="Archivo CSV de asientos contables")
    accounting_file_name = fields.Char(string="Nombre del archivo de asientos")

    # Campos comunes
    delimiter = fields.Char(string="Delimitador", default=";", help="Delimitador de archivos CSV")
    encoding = fields.Selection([
        ('utf-8', 'UTF-8'),
        ('latin-1', 'Latin-1 (ISO-8859-1)'),
        ('cp1252', 'Windows-1252'),
        ('utf-8-sig', 'UTF-8 con BOM')
    ], string="Codificación", default="latin-1",
        help="Seleccione la codificación del archivo CSV")
    ignore_errors = fields.Boolean(string="Ignorar errores de codificación",
                                   default=False,
                                   help="Activar para reemplazar caracteres no válidos")

    # Campos específicos para asientos contables
    journal_id = fields.Many2one(comodel_name='account.journal',
                                 string="Diario contable",
                                 domain=[('type', '=', 'general')],
                                 help="Diario donde se crearán los asientos contables")

    def action_import(self):
        """Import partners and/or accounting entries from CSV files."""
        result = {}
        partners_created = 0
        partners_skipped = 0
        entries_created = 0
        skipped_lines = 0

        self._convert_accounts_to_eigth_digits()

        if self.plan_csv_file:
            try:
                # Importar plan contable
                accounts_result = self._import_account_plan()
                accounts_created = accounts_result.get('accounts_created', 0)
                accounts_skipped = accounts_result.get('accounts_skipped', 0)
            except Exception as e:
                raise UserError(_("Error al procesar el archivo del plan contable: %s") % str(e))

        # Importar contactos si hay archivo seleccionado
        if self.contact_csv_file:
            try:
                # Código existente para importar contactos
                partners_result = self._import_partners()
                partners_created = partners_result.get('partners_created', 0)
                partners_skipped = partners_result.get('partners_skipped', 0)
                skipped_lines = partners_result.get('skipped_lines', 0)
            except Exception as e:
                raise UserError(_("Error al procesar el archivo de contactos: %s") % str(e))

        # # Importar asientos contables si hay archivo seleccionado
        if self.accounting_csv_file:
            if not self.journal_id:
                raise UserError(_("Por favor, seleccione un diario contable para importar los asientos."))

            try:
                entries_result = self._import_accounting_entries()
                entries_created = entries_result.get('entries_created', 0)
                entries_skipped = entries_result.get('entries_skipped', 0)
            except Exception as e:
                raise UserError(_("Error al procesar el archivo de asientos contables: %s") % str(e))

        # Mostrar mensaje de éxito
        message = ""
        if self.plan_csv_file:
            message += _("%s cuentas creadas. %s cuentas ya existían. ") % (
                accounts_created, accounts_skipped)

        if self.contact_csv_file:
            message += _("%s contactos creados. %s contactos ya existían. %s líneas ignoradas. ") % (
                partners_created, partners_skipped, skipped_lines)

        if self.accounting_csv_file:
            message += _("%s asientos contables creados. ") % entries_created

        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": _("Importación exitosa"),
                "message": message,
                "sticky": False,
                "type": "success",
                "next": {"type": "ir.actions.act_window_close"},
            }
        }

    def _convert_accounts_to_eigth_digits(self):
        """Convierte todas las cuentas contables existentes a 8 dígitos."""
        account_account_obj = self.env['account.account']
        accounts = account_account_obj.search([])

        for account in accounts:
            print("account", account)

            original_code = account.code

            # Si ya tiene 8 dígitos, no hacer nada
            if len(original_code) == 8:
                continue

            if len(original_code) < 8:
                # Rellenar con ceros a la derecha
                new_code = original_code.ljust(8, '0')
                is_account = account_account_obj.search([('code', '=', new_code)], limit=1)
                if not is_account:
                    account.code = new_code

    def _import_account_plan(self):
        """
        Importa el plan contable desde un archivo CSV.
        Excluye las cuentas que empiezan por 400, 410, 430, y las que ya existen.
        """
        accounts_created = 0
        accounts_skipped = 0

        if not self.plan_csv_file:
            return {
                'accounts_created': 0,
                'accounts_skipped': 0
            }

        try:
            # Procesar el archivo CSV
            csv_data = base64.b64decode(self.plan_csv_file)

            # Decodificar con la codificación seleccionada
            if self.ignore_errors:
                csv_text = csv_data.decode(self.encoding, errors='replace')
            else:
                csv_text = csv_data.decode(self.encoding)

            # Dividir el texto en líneas
            lines = csv_text.splitlines()

            account_account_obj = self.env['account.account']

            for line in lines:
                if not line.strip():
                    continue

                # Dividir la línea por el punto y coma
                parts = line.split(';')
                if len(parts) < 2:
                    continue

                code = parts[0].strip()
                name = parts[1].strip()

                if not code or not name:
                    continue

                # Verificar si el código de cuenta comienza con alguno de los prefijos excluidos
                excluded_prefixes = ["400", "410", "430"]
                if any(code.startswith(prefix) for prefix in excluded_prefixes):
                    accounts_skipped += 1
                    continue

                # Verificar si la cuenta ya existe
                existing_account = account_account_obj.search([('code', '=', code)], limit=1)
                if existing_account:
                    accounts_skipped += 1
                    continue

                # Determinar el tipo de cuenta según su código
                account_type = self._determine_account_type(code)

                # Crear la cuenta
                account_account_obj.create({
                    'code': code,
                    'name': name,
                    'account_type': account_type,
                    'company_ids': [(6, 0, [self.env.company.id])],
                })
                accounts_created += 1

            return {
                'accounts_created': accounts_created,
                'accounts_skipped': accounts_skipped
            }

        except Exception as e:
            raise UserError(_("Error al procesar el archivo del plan contable: %s") % str(e))

    def _determine_account_type(self, code):
        """
        Determina el tipo de cuenta según su código.
        """
        # Primeros dígitos del código de cuenta
        prefix = code[:1]

        # Mapeo de prefijos a tipos de cuenta para Odoo 17
        type_mapping = {
            '1': 'equity',  # Cuentas de capital
            '2': 'asset_non_current',  # Activo no corriente
            '3': 'asset_current',  # Existencias
            '4': 'liability_current',  # Pasivo
            '5': 'liability_current',  # Cuentas financieras
            '6': 'expense',  # Gastos
            '7': 'income',  # Ingresos
        }

        return type_mapping.get(prefix, 'asset_current')

    def _import_partners(self):
        """Procesa el archivo CSV de contactos y crea/actualiza los contactos en Odoo."""
        partners_created = 0
        partners_skipped = 0
        skipped_lines = 0

        if not self.contact_csv_file:
            return {
                'partners_created': 0,
                'partners_skipped': 0,
                'skipped_lines': 0
            }

        try:
            # Procesar el archivo CSV
            csv_data = base64.b64decode(self.contact_csv_file)

            # Decodificar con la codificación seleccionada
            if self.ignore_errors:
                csv_text = csv_data.decode(self.encoding, errors='replace')
            else:
                csv_text = csv_data.decode(self.encoding)

            csv_file = io.StringIO(csv_text)
            reader = csv.reader(csv_file, delimiter=self.delimiter)

            for row in reader:
                if not row or len(row) < 3:  # Necesitamos al menos 3 columnas
                    skipped_lines += 1
                    continue

                # Verificar si el código de cuenta (columna 2) comienza con prefijos permitidos
                allowed_prefixes = ["40", "41", "43"]
                if any(row[2].startswith(prefix) for prefix in allowed_prefixes):
                    vat = row[0].strip() if row[0].strip() else False
                    partner_name = row[1].strip() if len(row) > 1 else ""
                    ref = row[2].strip() if len(row) > 2 else ""
                    street = row[3].strip() if len(row) > 3 else ""
                    zip_code = row[4].strip() if len(row) > 4 else ""
                    city = row[5].strip() if len(row) > 5 else ""
                    state = row[6].strip() if len(row) > 6 else ""
                    country = row[7].strip() if len(row) > 7 else ""
                    phone = row[9].strip() if len(row) > 9 and row[9].strip() else ""

                    if partner_name:
                        # Verificar si el contacto ya existe
                        existing_partner = self.env["res.partner"].search([
                            "|",
                            ("name", "=ilike", partner_name),
                            ("vat", "=", vat)
                        ], limit=1)

                        if not existing_partner:
                            # Crear un nuevo contacto con información completa
                            partner_vals = {
                                "company_type": "company",
                                "name": partner_name,
                                "vat": vat,
                                "street": street,
                                "zip": zip_code,
                                "city": city,
                                "phone": phone,
                                "ref": ref,
                            }

                            # Si existe país, buscarlo
                            if country:
                                country_id = self.env["res.country"].search([
                                    "|",
                                    ("name", "=ilike", country),
                                    ("code", "=ilike", country)
                                ], limit=1)
                                if country_id:
                                    partner_vals["country_id"] = country_id.id

                            self.env["res.partner"].create(partner_vals)
                            partners_created += 1
                        else:
                            partners_skipped += 1

            return {
                'partners_created': partners_created,
                'partners_skipped': partners_skipped,
                'skipped_lines': skipped_lines
            }

        except Exception as e:
            raise UserError(_("Error al procesar el archivo de contactos: %s") % str(e))

    def _import_accounting_entries(self):
        """Process accounting entries CSV file."""
        entries_created = 0
        entries_skipped = 0

        # Procesar el archivo CSV
        csv_data = base64.b64decode(self.accounting_csv_file)

        # Decodificar con la codificación seleccionada
        if self.ignore_errors:
            csv_text = csv_data.decode(self.encoding, errors='replace')
        else:
            csv_text = csv_data.decode(self.encoding)

        # Preparar para procesar línea por línea
        lines = csv_text.splitlines()

        current_entry = None
        entry_lines = []
        entry_date = None
        entry_ref = None
        entry_number = None
        partner_id = None

        for line in lines:
            # Omitir líneas vacías
            if not line.strip():
                continue

            # Dividir la línea según el delimitador
            parts = line.split(self.delimiter)

            # Verificar si es encabezado de asiento
            if line.startswith('Asiento N'):
                # Si ya tenemos un asiento en proceso, guardarlo antes de comenzar uno nuevo
                if current_entry and entry_lines:
                    self._create_accounting_entry(entry_date, entry_number, entry_ref, entry_lines)
                    entries_created += 1
                    entry_lines = []

                # Extraer número de asiento
                if len(parts) >= 2:
                    entry_number = parts[1].strip()
                    current_entry = entry_number

            # Verificar si es una línea de asiento (fecha en formato DD-MM-YYYY)
            elif len(parts) >= 7 and self._is_date(parts[0]):
                date_str = parts[0].strip()
                line_number = parts[1].strip()
                account_code = parts[2].strip()
                description = parts[3].strip()
                concept = parts[4].strip()
                reference = parts[5].strip()

                # Extraer debe y haber
                debit = self._parse_amount(parts[6]) if parts[6].strip() else 0.0
                credit = self._parse_amount(parts[7]) if len(parts) > 7 and parts[7].strip() else 0.0

                # Guardar la fecha del asiento
                if not entry_date:
                    entry_date = self._parse_date(date_str)

                # Guardar la referencia del asiento
                if concept and not entry_ref:
                    entry_ref = concept

                if account_code and any(account_code.startswith(prefix) for prefix in ["400", "410", "430"]):
                    partner_id = self.env['res.partner'].search([('ref', '=', account_code)], limit=1)

                # Añadir línea al asiento actual
                entry_lines.append({
                    'account_code': account_code,
                    'name': description,
                    'debit': debit,
                    'credit': credit,
                    'ref': concept,
                })

            # Si es línea de total de asiento, ignorar
            elif line.startswith('Totales Asiento') and current_entry and entry_lines:
                self._create_accounting_entry(entry_date, entry_number, entry_ref, entry_lines, partner_id)
                entries_created += 1
                current_entry = None
                entry_lines = []
                entry_date = None
                entry_ref = None
                entry_number = None
                partner_id = None

            # Si es otro tipo de línea (cabecera, etc.), ignorar
            else:
                continue

        # Crear el último asiento si queda alguno pendiente

        return {
            'entries_created': entries_created,
            'entries_skipped': entries_skipped
        }

    def _create_accounting_entry(self, date, number, ref, lines, partner_id=None):
        """Create account.move with its lines."""
        account_move_obj = self.env['account.move']
        account_account_obj = self.env['account.account']

        # Valores para el asiento contable
        move_vals = {
            'date': date,
            'ref': f"{ref} - Asiento {number}" if ref else f"Asiento {number}",
            'journal_id': self.journal_id.id,
            'line_ids': [],
        }

        # Preparar líneas del asiento
        for line in lines:
            if line['account_code'].startswith(('400', '410', '430')):
                line['account_code'] = line['account_code'][:3] + '00000'

            # Buscar la cuenta contable
            account = account_account_obj.search([('code', '=', line['account_code'])], limit=1)
            if not account:
                continue

            # Añadir línea al asiento
            move_vals['line_ids'].append((0, 0, {
                'name': line['name'],
                'account_id': account.id,
                'partner_id': partner_id.id if partner_id else False,
                'debit': line['debit'],
                'credit': line['credit'],
                'ref': line['ref'],
            }))

        print("move_vals", move_vals)

        # Crear el asiento si hay líneas
        if move_vals['line_ids']:
            account_move_obj.create(move_vals)

    def _is_date(self, date_str):
        """Check if a string has date format DD-MM-YYYY."""
        try:
            if len(date_str.strip().split('-')) == 3:
                return True
            return False
        except:
            return False

    def _parse_date(self, date_str):
        """Convert date string to date object."""
        try:
            day, month, year = date_str.split('-')
            return fields.Date.to_date(f"{year}-{month}-{day}")
        except:
            # Si falla, devolver la fecha actual
            return fields.Date.today()

    def _parse_amount(self, amount_str):
        """Convert string amount to float, handling European format."""
        try:
            # Reemplazar coma por punto para decimales
            amount_str = amount_str.strip().replace('.', '').replace(',', '.')
            return float(amount_str or 0.0)
        except:
            return 0.0
