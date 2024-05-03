## Spaceport API
API service for spaceport managing written on DRF.



## Installation

Python 3.11 must be already installed.

```shell
git clone https://github.com/Mazur-Mariia-Python/spaceport-service
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
``` 
## Check it out
* Get access token via /api/user/token/.

   ```shell
   login: astronaut1@spacemail.com
   password: astronaut123
   ``` 

## Getting access
* Create user via /api/user/register/.
* Get access token via /api/user/token/.

## Features

* JWT authenticated.
* Admin panel /admin/.
* Documentation is located at /api/doc/swagger/ and /api/doc/redoc/.
* Managing orders and tickets.
* Creating spaceships with spaceship types, spaceship crews.
* Creating spaceflights.
* Creating routs with spaceports.
* Adding planets.

## DB structure
   
  ![img.png](diagram.png)

## Demo

Pages images:

1. Spaceship type list page.

   ![img.png](spaceship_types_list_page.png)

2. Spaceship type instance page.

   ![img.png](spaceship_types_instance_page.png)

3. Crew list page.

   ![img.png](crew_list_page.png)

4. Crew instance page.

   ![img.png](crew_instance_page.png)

5. Spaceship list page.

   ![img.png](spaceship_list_page.png)

6. Spaceship instance page.

   ![img.png](spaceship_instance_page.png)

7. Upload image page.

   ![img.png](upload_image_page.png)

8. Planet list page.

   ![img.png](planet_list_page.png)

9. Planet instance page.

    ![img.png](planet_instance_page.png)

10. Spaceport list page.

   ![img.png](spaceport_list_page.png)

11. Spaceport instance page.

   ![img.png](spaceport_instance_page.png)

12. Route list page.

   ![img.png](route_list_page.png)

13. Route instance page.

  ![img.png](route_instance_page.png)

14. Spaceflight list page.

   ![img.png](spaceflight_list_page.png)

15. Spaceflight instance page.

   ![img.png](spaceflight_instance_page.png)

16. Order list page.

   ![img.png](order_list_page.png)

17. Order instance page.

   ![img.png](order_instance_page.png)

18. Spaceship list page with crew filtering.

   ![img.png](spaceship_list_page-with_crew_filtering.png)

   ![img.png](spaceship_list_page-with_crew_filtering_1.png)

   ![img_1.png](spaceship_list_page-with_crew_filtering_2.png)
