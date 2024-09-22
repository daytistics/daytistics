-- Exported from QuickDBD: https://www.quickdatabasediagrams.com/
-- Link to schema: https://app.quickdatabasediagrams.com/#/d/xoyy8v
-- NOTE! If you have used non-SQL datatypes in your design, you will have to change these here.


-- Extended Django default user with important properties. You can find a list of all properties in the documentation (https://docs.djangoproject.com/en/5.1/ref/contrib/auth/
CREATE TABLE "CustomUser" (
    "id" int   NOT NULL,
    "email" email   NOT NULL,
    "username" string   NOT NULL,
    "password" string   NOT NULL,
    "activities" ActivityType   NOT NULL,
    CONSTRAINT "pk_CustomUser" PRIMARY KEY (
        "id"
     ),
    CONSTRAINT "uc_CustomUser_email" UNIQUE (
        "email"
    )
);

-- Model for a daytistic. Primarily serves as a node that bunde different models.
CREATE TABLE "Daytistic" (
    "id" int   NOT NULL,
    "date" date   NOT NULL,
    "user" user   NOT NULL,
    "diary" DiaryEntry   NULL,
    "activities" ActivityEntry   NOT NULL,
    "wellbeings" WellbeingEntry   NOT NULL,
    CONSTRAINT "pk_Daytistic" PRIMARY KEY (
        "id"
     )
);

-- Responsible for storing activity entries. One activity entry can belong to many daytistics, to save database storage. That means if a user creates an activity entry which does already exist the user is added to this entry.
CREATE TABLE "ActivityEntry" (
    "id" int   NOT NULL,
    "daytistic" Daytistic   NOT NULL,
    "type" ActivityType   NOT NULL,
    "start_time" date   NOT NULL,
    "end_time" date   NOT NULL,
    CONSTRAINT "pk_ActivityEntry" PRIMARY KEY (
        "id"
     )
);

-- Container model for the activity types (Work, Productivity, Sport, Health, Familie & Friends, Happiness, Recreation, Time For Me and Gratitude). Every user can add his own activities. If a user creates an activity which does already exists, the user is assigned to it.
CREATE TABLE "ActivityType" (
    "id" int   NOT NULL,
    "name" string   NOT NULL,
    "users" CustomUser   NOT NULL,
    CONSTRAINT "pk_ActivityType" PRIMARY KEY (
        "id"
     ),
    CONSTRAINT "uc_ActivityType_name" UNIQUE (
        "name"
    )
);

-- Responsible for storing well-being ratings. One wellbeing entry can belong to many daytistics, to save database storage. That means if a user creates an new daytistic and sets the well-being, a new entry is only created if not entry like this exists.
CREATE TABLE "WellbeingEntry" (
    "id" int   NOT NULL,
    "daytistic" Daytistic   NOT NULL,
    "type" WellbeingType   NOT NULL,
    "rating" int  DEFAULT 5 NOT NULL,
    CONSTRAINT "pk_WellbeingEntry" PRIMARY KEY (
        "id"
     )
);

-- Container model for predefined well-being types (Work, Productivity, Sport, Health, Familie & Friends, Happiness, Recreation, Time For Me and Gratitude). Stored in database to to make it easily expandable.
CREATE TABLE "WellbeingType" (
    "id" int   NOT NULL,
    "name" string   NOT NULL,
    CONSTRAINT "pk_WellbeingType" PRIMARY KEY (
        "id"
     )
);

-- Stores the diary entry which belongs to one daytistic.
CREATE TABLE "DiaryEntry" (
    "id" int   NOT NULL,
    "daytistic" Daytistic   NOT NULL,
    "entry" text   NOT NULL,
    "moment" text   NOT NULL,
    CONSTRAINT "pk_DiaryEntry" PRIMARY KEY (
        "id"
     )
);

ALTER TABLE "CustomUser" ADD CONSTRAINT "fk_CustomUser_activities" FOREIGN KEY("activities")
REFERENCES "ActivityType" ("");

ALTER TABLE "Daytistic" ADD CONSTRAINT "fk_Daytistic_user" FOREIGN KEY("user")
REFERENCES "CustomUser" ("");

ALTER TABLE "Daytistic" ADD CONSTRAINT "fk_Daytistic_diary" FOREIGN KEY("diary")
REFERENCES "DiaryEntry" ("");

ALTER TABLE "Daytistic" ADD CONSTRAINT "fk_Daytistic_activities" FOREIGN KEY("activities")
REFERENCES "ActivityEntry" ("");

ALTER TABLE "Daytistic" ADD CONSTRAINT "fk_Daytistic_wellbeings" FOREIGN KEY("wellbeings")
REFERENCES "WellbeingEntry" ("");

ALTER TABLE "ActivityEntry" ADD CONSTRAINT "fk_ActivityEntry_daytistic" FOREIGN KEY("daytistic")
REFERENCES "Daytistic" ("");

ALTER TABLE "ActivityEntry" ADD CONSTRAINT "fk_ActivityEntry_type" FOREIGN KEY("type")
REFERENCES "ActivityType" ("");

ALTER TABLE "ActivityType" ADD CONSTRAINT "fk_ActivityType_users" FOREIGN KEY("users")
REFERENCES "CustomUser" ("");

ALTER TABLE "WellbeingEntry" ADD CONSTRAINT "fk_WellbeingEntry_daytistic" FOREIGN KEY("daytistic")
REFERENCES "Daytistic" ("");

ALTER TABLE "WellbeingEntry" ADD CONSTRAINT "fk_WellbeingEntry_type" FOREIGN KEY("type")
REFERENCES "WellbeingType" ("");

ALTER TABLE "DiaryEntry" ADD CONSTRAINT "fk_DiaryEntry_daytistic" FOREIGN KEY("daytistic")
REFERENCES "Daytistic" ("");

CREATE INDEX "idx_Daytistic_date"
ON "Daytistic" ("date");

CREATE INDEX "idx_ActivityEntry_daytistic"
ON "ActivityEntry" ("daytistic");

CREATE INDEX "idx_WellbeingType_name"
ON "WellbeingType" ("name");

