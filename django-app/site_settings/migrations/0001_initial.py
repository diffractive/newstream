# Generated by Django 3.0.8 on 2020-08-21 10:56

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields
import wagtail.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailimages', '0022_uploadedimage'),
        ('wagtailcore', '0045_assign_unlock_grouppagepermission'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentGateway',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True)),
                ('frontend_label_attr_name', models.CharField(max_length=255)),
                ('list_order', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Payment Gateway',
                'verbose_name_plural': 'Payment Gateways',
                'ordering': ['list_order'],
            },
        ),
        migrations.CreateModel(
            name='SiteSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('default_from_email', models.EmailField(max_length=254)),
                ('signup_footer_text', wagtail.fields.RichTextField(blank=True)),
                ('signup_footer_text_en', wagtail.fields.RichTextField(blank=True, null=True)),
                ('signup_footer_text_zh_hant', wagtail.fields.RichTextField(blank=True, null=True)),
                ('signup_footer_text_ms', wagtail.fields.RichTextField(blank=True, null=True)),
                ('signup_footer_text_id_id', wagtail.fields.RichTextField(blank=True, null=True)),
                ('signup_footer_text_tl', wagtail.fields.RichTextField(blank=True, null=True)),
                ('sandbox_mode', models.BooleanField(default=True)),
                ('currency', models.CharField(choices=[('USD', 'US Dollars ($)'), ('EUR', 'Euros (€)'), ('GBP', 'Pounds Sterling (£)'), ('AUD', 'Australian Dollars ($)'), ('BRL', 'Brazilian Real (R$)'), ('CAD', 'Canadian Dollars ($)'), ('CZK', 'Czech Koruna (Kč)'), ('DKK', 'Danish Krone (\xa0kr.\xa0)'), ('HKD', 'Hong Kong Dollar ($)'), ('HUF', 'Hungarian Forint (Ft)'), ('ILS', 'Israeli Shekel (₪)'), ('JPY', 'Japanese Yen (¥)'), ('MYR', 'Malaysian Ringgits (RM)'), ('MXN', 'Mexican Peso ($)'), ('MAD', 'Moroccan Dirham (.د.م)'), ('NZD', 'New Zealand Dollar ($)'), ('NOK', 'Norwegian Krone (kr.)'), ('PHP', 'Philippine Pesos (₱)'), ('PLN', 'Polish Zloty (zł)'), ('SGD', 'Singapore Dollar ($)'), ('KRW', 'South Korean Won (₩)'), ('ZAR', 'South African Rand (R)'), ('SEK', 'Swedish Krona (\xa0kr.\xa0)'), ('CHF', 'Swiss Franc (CHF)'), ('TWD', 'Taiwan New Dollars (NT$)'), ('THB', 'Thai Baht (฿)'), ('INR', 'Indian Rupee (₹)'), ('TRY', 'Turkish Lira (₺)'), ('IRR', 'Iranian Rial (﷼)'), ('RUB', 'Russian Rubles (₽)'), ('AED', 'United Arab Emirates dirham (د.إ)'), ('AMD', 'Armenian dram (AMD)'), ('ANG', 'Netherlands Antillean guilder (ƒ)'), ('ARS', 'Argentine peso ($)'), ('AWG', 'Aruban florin (ƒ)'), ('BAM', 'Bosnia and Herzegovina convertible mark (KM)'), ('BDT', 'Bangladeshi taka (৳)'), ('BHD', 'Bahraini dinar (.د.ب)'), ('BMD', 'Bermudian dollar (BD$)'), ('BND', 'Brunei dollar (B$)'), ('BOB', 'Bolivian boliviano (Bs.)'), ('BSD', 'Bahamian dollar (B$)'), ('BWP', 'Botswana pula (P)'), ('BZD', 'Belizean dollar (BZ$)'), ('CLP', 'Chilean peso ($)'), ('CNY', 'Chinese yuan (¥)'), ('COP', 'Colombian peso ($)'), ('CRC', 'Costa Rican colón (₡)'), ('CUC', 'Cuban convertible peso (₱)'), ('CUP', 'Cuban convertible peso (₱)'), ('DOP', 'Dominican peso (RD$)'), ('EGP', 'Egyptian pound (E£)'), ('GIP', 'Gibraltar pound (£)'), ('GTQ', 'Guatemalan quetzal (Q)'), ('HNL', 'Honduran lempira (L)'), ('HRK', 'Croatian kuna (kn)'), ('IDR', 'Indonesian rupiah (Rp)'), ('ISK', 'Icelandic króna (kr)'), ('JMD', 'Jamaican dollar (j$)'), ('JOD', 'Jordanian dinar (د.ا)'), ('KES', 'Kenyan shilling (KSh)'), ('KWD', 'Kuwaiti dinar (د.ك)'), ('KYD', 'Cayman Islands dollar (KY$)'), ('MKD', 'Macedonian denar (ден)'), ('NPR', 'Nepalese rupee (₨)'), ('OMR', 'Omani rial (ر.ع.)'), ('PEN', 'Peruvian nuevo sol (S/.)'), ('PKR', 'Pakistani rupee (₨)'), ('RON', 'Romanian leu (L)'), ('SAR', 'Saudi riyal (ر.س)'), ('SZL', 'Swazi lilangeni (E)'), ('TOP', 'Tongan paʻanga (T$)'), ('TZS', 'Tanzanian shilling (TSh)'), ('UAH', 'Ukrainian hryvnia (₴)'), ('UYU', 'Uruguayan peso ($U)'), ('VEF', 'Venezuelan bolívar (Bs)'), ('XCD', 'East Caribbean dollar (EC$)'), ('AFN', 'Afghan afghani (؋)'), ('ALL', 'Albanian lek (L)'), ('AOA', 'Angolan kwanza (Kz)'), ('AZN', 'Azerbaijani manat (AZN)'), ('BBD', 'Barbadian dollar ($)'), ('BGN', 'Bulgarian lev (лв.)'), ('BIF', 'Burundian franc (Fr)'), ('BTC', 'Bitcoin (฿)'), ('BTN', 'Bhutanese ngultrum (Nu.)'), ('BYR', 'Belarusian ruble (old) (Br)'), ('BYN', 'Belarusian ruble (Br)'), ('CDF', 'Congolese franc (Fr)'), ('CVE', 'Cape Verdean escudo ($)'), ('DJF', 'Djiboutian franc (Fr)'), ('DZD', 'Algerian dinar (د.ج)'), ('ERN', 'Eritrean nakfa (Nfk)'), ('ETB', 'Ethiopian birr (Br)'), ('FJD', 'Fijian dollar ($)'), ('FKP', 'Falkland Islands pound (£)'), ('GEL', 'Georgian lari (₾)'), ('GGP', 'Guernsey pound (£)'), ('GHS', 'Ghana cedi (₵)'), ('GMD', 'Gambian dalasi (D)'), ('GNF', 'Guinean franc (Fr)'), ('GYD', 'Guyanese dollar ($)'), ('HTG', 'Haitian gourde (G)'), ('IMP', 'Manx pound (£)'), ('IQD', 'Iraqi dinar (ع.د)'), ('IRT', 'Iranian toman (تومان)'), ('JEP', 'Jersey pound (£)'), ('KGS', 'Kyrgyzstani som (сом)'), ('KHR', 'Cambodian riel (៛)'), ('KMF', 'Comorian franc (Fr)'), ('KPW', 'North Korean won (₩)'), ('KZT', 'Kazakhstani tenge (KZT)'), ('LAK', 'Lao kip (₭)'), ('LBP', 'Lebanese pound (ل.ل)'), ('LKR', 'Sri Lankan rupee (රු)'), ('LRD', 'Liberian dollar ($)'), ('LSL', 'Lesotho loti (L)'), ('LYD', 'Libyan dinar (ل.د)'), ('MDL', 'Moldovan leu (MDL)'), ('MGA', 'Malagasy ariary (Ar)'), ('MMK', 'Burmese kyat (Ks)'), ('MNT', 'Mongolian tögrög (₮)'), ('MOP', 'Macanese pataca (P)'), ('MRO', 'Mauritanian ouguiya (UM)'), ('MUR', 'Mauritian rupee (₨)'), ('MVR', 'Maldivian rufiyaa (.ރ)'), ('MWK', 'Malawian kwacha (MK)'), ('MZN', 'Mozambican metical (MT)'), ('NAD', 'Namibian dollar ($)'), ('NGN', 'Nigerian naira (₦)'), ('NIO', 'Nicaraguan córdoba (C$)'), ('PAB', 'Panamanian balboa (B/.)'), ('PGK', 'Papua New Guinean kina (K)'), ('PRB', 'Transnistrian ruble (р.)'), ('PYG', 'Paraguayan guaraní (₲)'), ('QAR', 'Qatari riyal (ر.ق)'), ('RSD', 'Serbian dinar (дин.)'), ('RWF', 'Rwandan franc (Fr)'), ('SBD', 'Solomon Islands dollar ($)'), ('SCR', 'Seychellois rupee (₨)'), ('SDG', 'Sudanese pound (ج.س.)'), ('SHP', 'Saint Helena pound (£)'), ('SLL', 'Sierra Leonean leone (Le)'), ('SOS', 'Somali shilling (Sh)'), ('SRD', 'Surinamese dollar ($)'), ('SSP', 'South Sudanese pound (£)'), ('STD', 'São Tomé and Príncipe dobra (Db)'), ('SYP', 'Syrian pound (ل.س)'), ('TJS', 'Tajikistani somoni (ЅМ)'), ('TMT', 'Turkmenistan manat (m)'), ('TND', 'Turkmenistan manat (د.ت)'), ('TTD', 'Trinidad and Tobago dollar ($)'), ('UGX', 'Ugandan shilling (UGX)'), ('UZS', 'Uzbekistani som (UZS)'), ('VND', 'Vietnamese đồng (₫)'), ('VUV', 'Vanuatu vatu (Vt)'), ('WST', 'Samoan tālā (T)'), ('XAF', 'Central African CFA franc (CFA)'), ('XOF', 'West African CFA franc (CFA)'), ('XPF', 'CFP franc (Fr)'), ('YER', 'Yemeni rial (﷼)'), ('ZMW', 'Zambian kwacha (ZK)')], default='USD', max_length=10)),
                ('_2c2p_frontend_label', models.CharField(default='2C2P(Credit Card)', help_text='The Gateway name to be shown on public-facing website.', max_length=255)),
                ('_2c2p_frontend_label_en', models.CharField(default='2C2P(Credit Card)', help_text='The Gateway name to be shown on public-facing website.', max_length=255, null=True)),
                ('_2c2p_frontend_label_zh_hant', models.CharField(default='2C2P(Credit Card)', help_text='The Gateway name to be shown on public-facing website.', max_length=255, null=True)),
                ('_2c2p_frontend_label_ms', models.CharField(default='2C2P(Credit Card)', help_text='The Gateway name to be shown on public-facing website.', max_length=255, null=True)),
                ('_2c2p_frontend_label_id_id', models.CharField(default='2C2P(Credit Card)', help_text='The Gateway name to be shown on public-facing website.', max_length=255, null=True)),
                ('_2c2p_frontend_label_tl', models.CharField(default='2C2P(Credit Card)', help_text='The Gateway name to be shown on public-facing website.', max_length=255, null=True)),
                ('_2c2p_merchant_id', models.CharField(blank=True, help_text='Merchant ID', max_length=255, null=True)),
                ('_2c2p_secret_key', models.CharField(blank=True, help_text='Secret Key', max_length=255, null=True)),
                ('_2c2p_testing_merchant_id', models.CharField(blank=True, help_text='Testing Merchant ID', max_length=255, null=True)),
                ('_2c2p_testing_secret_key', models.CharField(blank=True, help_text='Testing Secret Key', max_length=255, null=True)),
                ('paypal_frontend_label', models.CharField(default='PayPal', help_text='The Gateway name to be shown on public-facing website.', max_length=255)),
                ('paypal_frontend_label_en', models.CharField(default='PayPal', help_text='The Gateway name to be shown on public-facing website.', max_length=255, null=True)),
                ('paypal_frontend_label_zh_hant', models.CharField(default='PayPal', help_text='The Gateway name to be shown on public-facing website.', max_length=255, null=True)),
                ('paypal_frontend_label_ms', models.CharField(default='PayPal', help_text='The Gateway name to be shown on public-facing website.', max_length=255, null=True)),
                ('paypal_frontend_label_id_id', models.CharField(default='PayPal', help_text='The Gateway name to be shown on public-facing website.', max_length=255, null=True)),
                ('paypal_frontend_label_tl', models.CharField(default='PayPal', help_text='The Gateway name to be shown on public-facing website.', max_length=255, null=True)),
                ('stripe_frontend_label', models.CharField(default='Stripe', help_text='The Gateway name to be shown on public-facing website.', max_length=255)),
                ('stripe_frontend_label_en', models.CharField(default='Stripe', help_text='The Gateway name to be shown on public-facing website.', max_length=255, null=True)),
                ('stripe_frontend_label_zh_hant', models.CharField(default='Stripe', help_text='The Gateway name to be shown on public-facing website.', max_length=255, null=True)),
                ('stripe_frontend_label_ms', models.CharField(default='Stripe', help_text='The Gateway name to be shown on public-facing website.', max_length=255, null=True)),
                ('stripe_frontend_label_id_id', models.CharField(default='Stripe', help_text='The Gateway name to be shown on public-facing website.', max_length=255, null=True)),
                ('stripe_frontend_label_tl', models.CharField(default='Stripe', help_text='The Gateway name to be shown on public-facing website.', max_length=255, null=True)),
                ('social_login_enabled', models.BooleanField(default=True)),
                ('social_skip_signup', models.BooleanField(default=False)),
                ('google_login_enabled', models.BooleanField(default=True)),
                ('facebook_login_enabled', models.BooleanField(default=True)),
                ('twitter_login_enabled', models.BooleanField(default=True)),
                ('brand_logo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image')),
                ('site', models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, to='wagtailcore.Site')),
                ('site_icon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image')),
            ],
            options={
                'verbose_name': 'Site Setting',
                'verbose_name_plural': 'Site Settings',
            },
        ),
        migrations.CreateModel(
            name='UserMetaField',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('label', models.CharField(help_text='The label of the form field', max_length=255, verbose_name='label')),
                ('label_en', models.CharField(help_text='The label of the form field', max_length=255, null=True, verbose_name='label')),
                ('label_zh_hant', models.CharField(help_text='The label of the form field', max_length=255, null=True, verbose_name='label')),
                ('label_ms', models.CharField(help_text='The label of the form field', max_length=255, null=True, verbose_name='label')),
                ('label_id_id', models.CharField(help_text='The label of the form field', max_length=255, null=True, verbose_name='label')),
                ('label_tl', models.CharField(help_text='The label of the form field', max_length=255, null=True, verbose_name='label')),
                ('field_type', models.CharField(choices=[('singleline', 'Single line text'), ('multiline', 'Multi-line text'), ('email', 'Email'), ('number', 'Number'), ('url', 'URL'), ('checkbox', 'Checkbox'), ('checkboxes', 'Checkboxes'), ('dropdown', 'Drop down'), ('multiselect', 'Multiple select'), ('radio', 'Radio buttons'), ('date', 'Date'), ('datetime', 'Date/time'), ('hidden', 'Hidden field')], max_length=16, verbose_name='field type')),
                ('required', models.BooleanField(default=True, verbose_name='required')),
                ('choices', models.TextField(blank=True, help_text='Comma separated list of choices. Only applicable in checkboxes, radio and dropdown.', verbose_name='choices')),
                ('choices_en', models.TextField(blank=True, help_text='Comma separated list of choices. Only applicable in checkboxes, radio and dropdown.', null=True, verbose_name='choices')),
                ('choices_zh_hant', models.TextField(blank=True, help_text='Comma separated list of choices. Only applicable in checkboxes, radio and dropdown.', null=True, verbose_name='choices')),
                ('choices_ms', models.TextField(blank=True, help_text='Comma separated list of choices. Only applicable in checkboxes, radio and dropdown.', null=True, verbose_name='choices')),
                ('choices_id_id', models.TextField(blank=True, help_text='Comma separated list of choices. Only applicable in checkboxes, radio and dropdown.', null=True, verbose_name='choices')),
                ('choices_tl', models.TextField(blank=True, help_text='Comma separated list of choices. Only applicable in checkboxes, radio and dropdown.', null=True, verbose_name='choices')),
                ('default_value', models.CharField(blank=True, help_text='Default value. Comma separated values supported for checkboxes.', max_length=255, verbose_name='default value')),
                ('default_value_en', models.CharField(blank=True, help_text='Default value. Comma separated values supported for checkboxes.', max_length=255, null=True, verbose_name='default value')),
                ('default_value_zh_hant', models.CharField(blank=True, help_text='Default value. Comma separated values supported for checkboxes.', max_length=255, null=True, verbose_name='default value')),
                ('default_value_ms', models.CharField(blank=True, help_text='Default value. Comma separated values supported for checkboxes.', max_length=255, null=True, verbose_name='default value')),
                ('default_value_id_id', models.CharField(blank=True, help_text='Default value. Comma separated values supported for checkboxes.', max_length=255, null=True, verbose_name='default value')),
                ('default_value_tl', models.CharField(blank=True, help_text='Default value. Comma separated values supported for checkboxes.', max_length=255, null=True, verbose_name='default value')),
                ('help_text', models.CharField(blank=True, max_length=255, verbose_name='help text')),
                ('help_text_en', models.CharField(blank=True, max_length=255, null=True, verbose_name='help text')),
                ('help_text_zh_hant', models.CharField(blank=True, max_length=255, null=True, verbose_name='help text')),
                ('help_text_ms', models.CharField(blank=True, max_length=255, null=True, verbose_name='help text')),
                ('help_text_id_id', models.CharField(blank=True, max_length=255, null=True, verbose_name='help text')),
                ('help_text_tl', models.CharField(blank=True, max_length=255, null=True, verbose_name='help text')),
                ('parent', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_meta_fields', to='site_settings.SiteSettings')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AdminEmails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('setting_parent', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='admin_emails', to='site_settings.SiteSettings')),
            ],
        ),
    ]
