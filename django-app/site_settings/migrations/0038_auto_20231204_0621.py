# Generated by Django 3.2.23 on 2023-12-04 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_settings', '0037_auto_20230613_0927'),
    ]

    operations = [
        migrations.AlterField(
            model_name='i18nabstractformfield',
            name='choices',
            field=models.TextField(blank=True, help_text='Comma or new line separated list of choices. Only applicable in checkboxes, radio and dropdown.', verbose_name='choices'),
        ),
        migrations.AlterField(
            model_name='i18nabstractformfield',
            name='default_value',
            field=models.TextField(blank=True, help_text='Default value. Comma or new line separated values supported for checkboxes.', verbose_name='default value'),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='currency',
            field=models.CharField(choices=[('None', 'None'), ('USD', 'US Dollars ($)'), ('EUR', 'Euros (€)'), ('GBP', 'Pounds Sterling (£)'), ('AUD', 'Australian Dollars ($)'), ('BRL', 'Brazilian Real (R$)'), ('CAD', 'Canadian Dollars ($)'), ('CZK', 'Czech Koruna (Kč)'), ('DKK', 'Danish Krone (\xa0kr.\xa0)'), ('HKD', 'Hong Kong Dollar ($)'), ('HUF', 'Hungarian Forint (Ft)'), ('ILS', 'Israeli Shekel (₪)'), ('JPY', 'Japanese Yen (¥)'), ('MYR', 'Malaysian Ringgits (RM)'), ('MXN', 'Mexican Peso ($)'), ('MAD', 'Moroccan Dirham (.د.م)'), ('NZD', 'New Zealand Dollar ($)'), ('NOK', 'Norwegian Krone (kr.)'), ('PHP', 'Philippine Pesos (₱)'), ('PLN', 'Polish Zloty (zł)'), ('SGD', 'Singapore Dollar ($)'), ('KRW', 'South Korean Won (₩)'), ('ZAR', 'South African Rand (R)'), ('SEK', 'Swedish Krona (\xa0kr.\xa0)'), ('CHF', 'Swiss Franc (CHF)'), ('TWD', 'Taiwan New Dollars (NT$)'), ('THB', 'Thai Baht (฿)'), ('INR', 'Indian Rupee (₹)'), ('TRY', 'Turkish Lira (₺)'), ('RUB', 'Russian Rubles (₽)'), ('AED', 'United Arab Emirates dirham (د.إ)'), ('AMD', 'Armenian dram (AMD)'), ('ANG', 'Netherlands Antillean guilder (ƒ)'), ('ARS', 'Argentine peso ($)'), ('AWG', 'Aruban florin (ƒ)'), ('BAM', 'Bosnia and Herzegovina convertible mark (KM)'), ('BDT', 'Bangladeshi taka (৳)'), ('BMD', 'Bermudian dollar (BD$)'), ('BND', 'Brunei dollar (B$)'), ('BOB', 'Bolivian boliviano (Bs.)'), ('BSD', 'Bahamian dollar (B$)'), ('BWP', 'Botswana pula (P)'), ('BZD', 'Belizean dollar (BZ$)'), ('CLP', 'Chilean peso ($)'), ('CNY', 'Chinese yuan (¥)'), ('COP', 'Colombian peso ($)'), ('CRC', 'Costa Rican colón (₡)'), ('DOP', 'Dominican peso (RD$)'), ('EGP', 'Egyptian pound (E£)'), ('GIP', 'Gibraltar pound (£)'), ('GTQ', 'Guatemalan quetzal (Q)'), ('HNL', 'Honduran lempira (L)'), ('HRK', 'Croatian kuna (kn)'), ('IDR', 'Indonesian rupiah (Rp)'), ('ISK', 'Icelandic króna (kr)'), ('JMD', 'Jamaican dollar (j$)'), ('KES', 'Kenyan shilling (KSh)'), ('KYD', 'Cayman Islands dollar (KY$)'), ('MKD', 'Macedonian denar (ден)'), ('NPR', 'Nepalese rupee (₨)'), ('PEN', 'Peruvian nuevo sol (S/.)'), ('PKR', 'Pakistani rupee (₨)'), ('RON', 'Romanian leu (L)'), ('SAR', 'Saudi riyal (ر.س)'), ('SZL', 'Swazi lilangeni (E)'), ('TOP', 'Tongan paʻanga (T$)'), ('TZS', 'Tanzanian shilling (TSh)'), ('UAH', 'Ukrainian hryvnia (₴)'), ('UYU', 'Uruguayan peso ($U)'), ('XCD', 'East Caribbean dollar (EC$)'), ('AFN', 'Afghan afghani (؋)'), ('ALL', 'Albanian lek (L)'), ('AOA', 'Angolan kwanza (Kz)'), ('AZN', 'Azerbaijani manat (AZN)'), ('BBD', 'Barbadian dollar ($)'), ('BGN', 'Bulgarian lev (лв.)'), ('BIF', 'Burundian franc (Fr)'), ('CDF', 'Congolese franc (Fr)'), ('CVE', 'Cape Verdean escudo ($)'), ('DJF', 'Djiboutian franc (Fr)'), ('DZD', 'Algerian dinar (د.ج)'), ('ETB', 'Ethiopian birr (Br)'), ('FJD', 'Fijian dollar ($)'), ('FKP', 'Falkland Islands pound (£)'), ('GEL', 'Georgian lari (₾)'), ('GMD', 'Gambian dalasi (D)'), ('GNF', 'Guinean franc (Fr)'), ('GYD', 'Guyanese dollar ($)'), ('HTG', 'Haitian gourde (G)'), ('KGS', 'Kyrgyzstani som (сом)'), ('KHR', 'Cambodian riel (៛)'), ('KMF', 'Comorian franc (Fr)'), ('KZT', 'Kazakhstani tenge (KZT)'), ('LAK', 'Lao kip (₭)'), ('LBP', 'Lebanese pound (ل.ل)'), ('LKR', 'Sri Lankan rupee (රු)'), ('LRD', 'Liberian dollar ($)'), ('LSL', 'Lesotho loti (L)'), ('MDL', 'Moldovan leu (MDL)'), ('MGA', 'Malagasy ariary (Ar)'), ('MMK', 'Burmese kyat (Ks)'), ('MNT', 'Mongolian tögrög (₮)'), ('MOP', 'Macanese pataca (P)'), ('MRO', 'Mauritanian ouguiya (UM)'), ('MUR', 'Mauritian rupee (₨)'), ('MVR', 'Maldivian rufiyaa (.ރ)'), ('MWK', 'Malawian kwacha (MK)'), ('MZN', 'Mozambican metical (MT)'), ('NAD', 'Namibian dollar ($)'), ('NGN', 'Nigerian naira (₦)'), ('NIO', 'Nicaraguan córdoba (C$)'), ('PAB', 'Panamanian balboa (B/.)'), ('PGK', 'Papua New Guinean kina (K)'), ('PYG', 'Paraguayan guaraní (₲)'), ('QAR', 'Qatari riyal (ر.ق)'), ('RSD', 'Serbian dinar (дин.)'), ('RWF', 'Rwandan franc (Fr)'), ('SBD', 'Solomon Islands dollar ($)'), ('SCR', 'Seychellois rupee (₨)'), ('SHP', 'Saint Helena pound (£)'), ('SLL', 'Sierra Leonean leone (Le)'), ('SOS', 'Somali shilling (Sh)'), ('SRD', 'Surinamese dollar ($)'), ('STD', 'São Tomé and Príncipe dobra (Db)'), ('TJS', 'Tajikistani somoni (ЅМ)'), ('TTD', 'Trinidad and Tobago dollar ($)'), ('UGX', 'Ugandan shilling (UGX)'), ('UZS', 'Uzbekistani som (UZS)'), ('VND', 'Vietnamese đồng (₫)'), ('VUV', 'Vanuatu vatu (Vt)'), ('WST', 'Samoan tālā (T)'), ('XAF', 'Central African CFA franc (CFA)'), ('XOF', 'West African CFA franc (CFA)'), ('XPF', 'CFP franc (Fr)'), ('YER', 'Yemeni rial (﷼)'), ('ZMW', 'Zambian kwacha (ZK)')], default='None', max_length=10),
        ),
    ]