admins_names = r'^.*(krashu|vincy|krewka|aplik|) (jestes|jesteś)\??'
admins = r'.*jest\s+ktoś\s+z\s+adm\b|jest\s+ktos\s+z\s+adm\b|administrator\s+dostepny\b|administrator\s+dostępny\b'
admins_ans = 'Dostępność administratorów możesz sprawdzić na naszej stronie.'

converter = r'^.*jaki (jest)? przelicznik|kurs\??'
converter_ans = 'Kursy można sprawdzić na naszej stronie internetowej'

sell_won = r'^.*sprzedam (won|wony)'

issue = r'^.*(mam problem)|((chciałbym|chcialbym) (zgłosić|zglosic|zgłosic|zglosić))'
issue_ans = 'Zgłoszenia przyjmujemy na supporcie lub w wiadomości prywatnej na discordzie'
