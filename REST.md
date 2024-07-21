# Kommunikation zwischen Frontend und Backend

## Authentication
Enthält Funktionen rund um Login, Registrierung & User-Management.


### Exists-Verification-Request

Die Exists-Verification-Action überprüft, ob aktuell im Verificator-Objekt, eine Anfrage des gegebenen Typs des Benutzers vorliegt.

**Adresse**: /user/verify/exists<br>
**Typ**: POST<br>

**Erwartet**:
- **Email** des Benutzers
- **Typ der Verifizierung**: Registrierung (1), Passwort ändern (2), Account löschen (3), Passwort zurücksetzen (4)

**Rückgabe**: 
- `{exists: False}, 200`, wenn aktuell keine Anfrage des gegebenen Typs für den Benutzer existiert.
- `{exists: True}, 200`, wenn bereits eine Anfrage des gegbenen Typs für den Benutzer existiert. 

### Verify-Action
Über die Verify-Action, lassen sich verifizierungsbedürftige Aktionen verifizieren. Nach der Verifizierung werden die zu verifizierenden Aktionen automatisch ausgeführt.

**Adresse**: /user/verify/<br>
**Typ**: POST<br>

**Erwartet**:
- **Email** des Benutzers
- **Typ der Verifizierung**: Registrierung (1), Passwort ändern (2), Account löschen (3), Passwort zurücksetzen (4)
- **Verifzierungscode**, der zuvor per Email versendet wurde

**Rückgabe**: 
- `{"message": "Verify-Action completed"}, 200`, wenn die Verifizierung erfolgreich ist


### User-Registration
Bei der User-Registration, wird eine neue Verifizierungsanfrage erstellt, bei deren Bestätigung ein neuer Benutzer erstellt wird. 

**Adresse**: /user/register<br>
**Typ**: POST<br>

**Erwartet**:
- **Benutzername** des Benutzers
- **Email** des Benutzers
- **Unverschlüsseltes Passwort** des Benutzers<br>
**‼️** Die unverschlüsselte Versendung des Passwortes ist in der Production nur unter HTTPS zulässig!

**Rückgabe**: 
- `{"message": "Registration request sent"}, 200`, wenn die Registrierungsanfrage erfolgreich versendet wurde