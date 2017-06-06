CREATE TABLE "library" (
	"id" serial(10) NOT NULL,
	"book" integer(10) NOT NULL,
	"author" integer(10) NOT NULL,
	CONSTRAINT library_pk PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "books" (
	"id" serial(10) NOT NULL,
	"book" varchar(100) NOT NULL,
	CONSTRAINT books_pk PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "authors" (
	"id" serial(10) NOT NULL,
	"author" varchar(100) NOT NULL,
	CONSTRAINT authors_pk PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



ALTER TABLE "library" ADD CONSTRAINT "library_fk0" FOREIGN KEY ("book") REFERENCES "books"("id");
ALTER TABLE "library" ADD CONSTRAINT "library_fk1" FOREIGN KEY ("author") REFERENCES "authors"("id");



