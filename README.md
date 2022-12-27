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

### Easy tasks
* [ ] Add autosave
* [ ] add column-points/points-cell CSS
* [x] implement competitions
  * [ ] Redirect to competition after creation
  * [x] Edit
  * etc

### Hard tasks
* [ ] Add security
* [ ] Add participation points
* [ ] competition and event details editing after creation
* [ ] Implement archival to everything
  * [x] Add restore button to archived results

### Completed tasks
* [x] list all competitions in event
* [x] implement events

## Planning
### `results` table
| id PK | race_id FK | student_id | score |
| ----- | ---------- | ---------- | ----- |
