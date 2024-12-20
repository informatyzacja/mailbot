# MailBot

MailBot służy do wysyłania automatycznie maili o określonej treści do odbiorców, którzy są zapisani w pliku txt.

## Konfiguracja

### Struktura pliku konfiguracyjnego

- `mail` - adres e-mail nadawcy
- `password` - hasło nadawcy
- `host` - adres serwera mailowego
- `port` - port SMTP serwera
- `mails_txt_file` - nazwa pliku `.txt` w katalogu `data` zawierająca listę maili wraz z użytkownikami, którzy mają być końcowymi odbiorcami wiadomości (struktura pliku poniżej)
- `mails_json_file` - nazwa pliku `.json` (w katalogu `data`), do której ma być zapisana struktura danych zawierająca nazwy użytkowników, adresy e-mail oraz ich UUID
- `subject` - temat wiadomości
- `mail_template` - nazwa pliku `.txt`, w którym jest szablon wiadomości przesyłanej do użytkowników (struktura pliku poniżej)
- `date` - data zakończenia ewidencji
- `attachments_subject` - temat wiadomości zwrotnej do nadawcy zawierającej załączniki z wynikami działania bota
- `attachment_mail_text` - tekst powyższej wiadomości
- `confirm_link` - link do strony służącej do potwierdzania użytkowników z przygotowanym już wcześniej polem w adresie do przyjęcia żądania `HTTP GET`

### Szablon pliku pod `mails_txt_file`

Pojedynczy rekord danych powinien wyglądać następująco:

    mail: <mail użytkownika>

Rekordów może być dowolna ilość, wszystko poza tym schematem zostanie zignorowane.

### Szablon pliku pod `mail_template`

Treść pliku może być dowolna, istnieją ponadto dwa literały podmiany indywidualizujące treść maila:

- `{mail}` jest zamieniane w treści maila na nazwę danego użytkownika z pliku
- `{date}` jest zamienane na podaną datę zakończenia ewidencji
- `{confirm_link}` jest zamienane na podany link wraz z dodanym UUID danego użytkownika

## Kroki konfiguracji

1. Przekopiuj plik `config/config.json.example` jako `config/config.json`.
2. Wprowadź swoją konfigurację do utworzonego wyżej pliku.
3. Postąp tak samo w przypadku pliku zapisanego pod `mail_template`.
4. Utwórz katalog `data`, po czym umieść w nim plik zapisany pod `mails_txt_file`.

## Uruchamianie

Wystarczy wpisać polecenie:

    ./mailbot.py

Po wysłaniu maili do wszystkich podanych odbiorców następuje wysłanie maila z załącznikami o wynikach działania bota do nadawcy tych wiadomości - co zabezpiecza przed sytuacją stracenia wszystkich danych przez ponowne uruchomienie bota.

## Po uruchomieniu

Te pliki zawierają dane potrzebne do dalszego etapu ewidencji maili

- `data/mails.json` - struktura danych zawierająca niezbędne UUID
- `logs/logs.log` - logi, w których są zawarte informacje dlaczego nie udało się wysłać maila
- `logs/sent.log` - lista adresów, na które udało się wysłać mail
- `logs/notsent.log` - lista adresów, na które nie udało się wysłać maila
