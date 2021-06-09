#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main(int argc, char* argv[])
{
    const char* db = "db.sqlite3";
    const char* migration_dir = "api/migrations";
    const char* website_migration = "website/migrations";


    if (access(db, F_OK) == 0) 
        system("rm db.sqlite3");
    
    if (access(migration_dir, F_OK) == 0) 
        system("rm -rf api/migrations");

    if (access(website_migration, F_OK) == 0)
	system("rm -rf website/migrations");
    
    const char* usr_creation = "echo \"from django.contrib.auth.models import User; User.objects.create_superuser('test', 'test@example.com', 'pass')\" | python3 manage.py shell";
    fprintf(stdin, "Created user ---> username = test | password = pass");
    system("python3 manage.py crontab add");
    system("python3 manage.py makemigrations");
    system("python3 manage.py makemigrations api");
    system("python3 manage.py makemigrations website");
    system("python3 manage.py migrate");
    system(usr_creation);
    system("python3 manage.py runserver");
    
    return 0;
}
