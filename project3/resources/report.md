# CMPE321 Project 3 Report

#### Bahadır Gezer - 2020400039
#### Simar Ahmet Kahya - 2020400378

## Schema Refinement

To begin with, I have critically analyzed our original schema from Project 1 in terms of functional dependencies and normalization. This led to several adjustments that I have introduced to refine our schema and meet the required BCNF or 3NF normal forms. Now, let's go through the changes one by one.

1. **Introduction of `user` table**: Our original schema included duplicate username, password, name, and surname fields across `Audience` and `Director` tables. This redundancy violates the principles of BCNF because it creates a transitive dependency where the password, name, and surname of a user depends on the username. To overcome this, I introduced a new `user` table that holds these shared fields, removing redundancy and ensuring adherence to BCNF. Now, the `user` table uniquely identifies every user by `username` with no transitive dependencies.

2. **Introduction of `nation` table**: Previously, we stored `nation` as a field directly in the `Director` table, which limited us in terms of managing distinct nations. In the updated schema, `nation` is managed in its own table, with a foreign key in the `director` table, providing a clear functional dependency (`username -> nation_id`) and meeting BCNF requirements.

3. **Decomposing `Director` table**: To further normalize, we separated the `Director` table into `director` and `director_platform`. In our original design, `Director` was not in BCNF due to the partial dependency of `platform_id` on `username`. By decomposing the table, we establish a clear functional dependency in `director_platform` (`director_username -> platform_id`), satisfying BCNF.

4. **Refining `Movie` table**: Our previous `Movie` table was not in BCNF because the `overall_rating` attribute was dependent on `id` and `director_name`. In our revised schema, `Movie` is in BCNF with functional dependencies `id -> name, duration, director_username`.

5. **Separation of `Movie_Genre`**: We continue to maintain the `Movie_Genre` relation as it was in BCNF previously and remains so.

6. **Changes in `Movie_Session`**: The `Movie_Session` table was refined to only have dependencies on `id -> time_slot, date, movie_id, theater_id`, maintaining BCNF.

7. **Restructuring `Rating`, `Subscription`, `Ticket`**: These tables were restructured to keep in line with the new `user` table and to maintain BCNF, where all non-key attributes are dependent on the key, and there are no transitive dependencies.

Regarding constraints, we have introduced CHECK constraints in various tables. For example, we are now ensuring that `average_rating` in the `movie` table cannot be negative and `capacity` in the `theater` table must be a positive integer. Additionally, we make sure that `time_slot` in the `movie_session` table is within a certain range. These constraints weren't captured in our previous schema and are now appropriately handled.

In conclusion, the refined schema is more robust, normalized to BCNF or 3NF, and effectively captures the constraints that we were not able to handle in Project 1.