# Car Intelligence



## Postgresql
    
Run the docker with following command

      docker run -itd -e POSTGRES_USER=madamec -e POSTGRES_PASSWORD=madamec -p 5432:5432 -v "C:\Users\Nasťa\Desktop\projects\CarIntelligence\db_data:/var/lib/postgresql/data" --name postgresql postgres


## Car information

On preview

| Name            | Type      | Description                            |
|-----------------|-----------|----------------------------------------|
| url             | str       | url to car detail page                 |
| image           | str       | url to the image                       |
| esa_id          | str       | identifier located in url              |
| brand           | str       | brand of the car                       |
| full_name       | str       | full name of the car                   |
| engine          | str       | type of the engine                     |
| equipment_class | str       | Equipment class of the car             |
| year            | int       | Year of assembly                       |
| gear            | str       | Type of gear                           |
| power           | int       | Power in kilowatts                     |
| fuel            | str       | Type of fuel                           |
| body            | str       | Type of body of the car                |
| mileage         | int       | Number of kilometers on tachometer     |
| lowcost         | boolean   | is the car tagged as lowcost           |
| premium         | boolean   | is the car tagged as premium           |
| monthly price   | int       | price with financing monthly           |
| special price   | int       | total price with financing             |
| tags            | list[str] | tags associated with the car equipment |
| condition       | float     | scoring of the quality from the seller |
| price           | int       | total price with one payment           |
| discount        | int       | total discount from original price     |


List of brands

| Brands         |
|----------------|
| Alfa Romeo     |
| Audi           |
| BMW            |
| Chevrolet      |
| Citroën        |
| Dacia          |
| Dodge          |
| Dongfeng       |
| DS Automobiles |
| Fiat           |
| Ford           |
| Honda          |
| Hyundai        |
| Jaguar         |
| Jeep           |
| Kia            |
| Lada           |
| Lancia         |
| Land Rover     |
| Mazda          |
| Mercedes-Benz  |
| Mini           |
| Mitsubishi     |
| Nissan         |
| Opel           |
| Peugeot        |
| Renault        |
| Rover          |
| Seat           |
| Škoda          |
| Smart          |
| SsangYong      |
| Subaru         |
| Suzuki         |
| Toyota         |
| Volkswagen     |
| Volvo          |

Types of car bodies

| Body             |
|------------------|
| kombi            |
| hatchback        |
| sedan            |
| liftback         |
| MPV              |
| SUV              |
| chladící-mrazící |
| kabriolet        |
| kupé             |
| minibus          |
| sklápěč          |
| pick up          |
| skříň            |
| užitkové vozidlo |
| valník           |
| VAN              |
