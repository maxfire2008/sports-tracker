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
* [ ] Implement archival to everything
  * [x] Add restore button to archived results
* [x] implement events
* [ ] Add security
* [ ] Add participation points
* [ ] Add autosave
* [ ] competition and event details editing after creation
* [ ] add column-points/points-cell CSS

## Planning
### `results` table
| id PK | race_id FK | student_id | score |
| ----- | ---------- | ---------- | ----- |
