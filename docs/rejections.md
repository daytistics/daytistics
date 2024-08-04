# Rejections
Eine Rejection bei Daytistics ist mit einem Communityauschluss gleichzusetzen. Dieser kann bei einer Sperrung durch das System oder einen Moderator, aber auch bei temporären Ausschlüssen von gewissen Features aufgrund von z.B. zu vielen Fehleingaben auftreten.

## Struktur
Rejections werden in der PostgreSQL-Tabelle "rejections" gespeichert. Diese enthält die folgenden Columns:
- **ID (id)**: ID der Rejection; zählt automatisch aufwärts
- **User ID (user_id)***: Fremdschlüssel zur ID des gesperrten Benutzers
- **Scope (scope)**: Bereich der Anwendung, in dem die Rejection gültig ist
- **Reason (reason)**: Grund für die Rejection
- **Duration (duration)**: Dauer der Rejection
- **Created At (created_at)**: Erstellungszeitpunkt der Rejection

## Dateien
Die Dateien welche sich mit Rejections behandeln, sind die folgenden:
- `backend/core/models/rejections.py`: Datenbankmodell für Rejections, sowie Funktionen, um Rejections zu bearbeiten
- `backend/core/services/rejections.py`: Enthält den Singelton `Rejection`, der sich um das entfernen abgelaufener Rejections kümmert. Dieser sollte über `backend/core/services/Rejector` importiert werden
