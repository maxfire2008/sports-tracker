# sports-tracker
## :construction: This software is in active development
Track sports carnivals!

## Database compatibility
* :x: SQLite
  * Doesn't work with the foreign key constraints. This could introduce bugs
* :construction: postgresql
  * development database
* :question: MySQL
  * unknown

## To-do
* [x] list all competitions in event
* [x] implement competitions
  * [ ] Redirect to competition after creation
  * [x] Edit
  * etc
* [x] Add restore button to archived items
* [x] implement events
* [ ] Add participation points
* [ ] Add autosave

## Planning
### `results` table
| id PK | race_id FK | student_id | score |
| ----- | ---------- | ---------- | ----- |
