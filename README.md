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
* [ ] implement competitions
* [ ] Add restore button to archived items
* [ ] implement events

## Planning
### `results` table
| id PK | race_id FK | student_id | score |
| ----- | ---------- | ---------- | ----- |
