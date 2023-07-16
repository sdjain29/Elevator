# Elevator

The Elevator System is a Django-based project that simulates an elevator system with various functionalities such as moving up and down, opening and closing doors, handling user requests, and managing the operational status of elevators.

## Architecture

The Elevator System follows a client-server architecture with a Django server as the backend and a client application (not provided) interacting with the server via RESTful APIs. The Django REST Framework (DRF) is used to develop the APIs, and PostgreSQL is used as the database.


The `apis` directory contains the Django views for handling various API endpoints, while the `elevator_system` directory contains the Django project settings and URL configurations. The `elevator` directory contains the Django models and serializers for the Elevator and Request objects.

## Database Modeling

The Elevator System uses a PostgreSQL database to store the elevator and request data. The primary models are `Elevator` and `Request`, with a one-to-many relationship where an elevator can have multiple requests. The `Elevator` model includes fields such as `current_floor`, `current_direction`, `is_operational`, and `is_open`, while the `Request` model includes fields such as `elevator`, `floor`, and `status`.

## API Contracts

The Elevator System exposes the following APIs:

- `POST /api/elevator/initialize/`: Initializes the elevator system by creating 'n' elevators.
- `GET /api/elevator/{elevator_id}/requests/`: Fetches all requests for a given elevator.
- `GET /api/elevator/{elevator_id}/next_destination/`: Fetches the next destination floor for a given elevator.
- `GET /api/elevator/{elevator_id}/current_direction/`: Fetches whether the elevator is currently moving up or down.
- `POST /api/elevator/{elevator_id}/save_request/`: Saves a user request to the list of requests for a specific elevator.
- `POST /api/elevator/{elevator_id}/set_operational/`: Sets the operational status of an elevator.
- `POST /api/elevator/call/`: Call elevator from external button.
- `POST /api/elevator/{elevator_id}/door_action/`: Sets the operational status of an elevator.

Please refer to the Postman Collection in the mail for detailed request and response structures.

## Setup, Deploy, and Test

To set up, deploy, and test the Elevator System, follow these steps:

1. Clone the repository: `git clone https://github.com/sdjain29/Elevator.git`
2. Install the dependencies: `pip install -r requirements.txt`
3. Configure the database settings in `elevator_project/settings.py`.
4. Apply migrations to create the necessary database tables: `python manage.py migrate`.
5. Start the server: `python manage.py runserver`.
6. Use a Postman Collection(in above repository) to send API requests to the server. (host = localhost:8000)
7. Refer to the API contracts for the required endpoints and request structures.
8. Test the system by making requests to the various API endpoints and verifying the responses.

## Libraries and Plugins Used

The Elevator System uses the following libraries and plugins:

- Django: The web framework used to develop the server-side application.
- Django REST Framework: A powerful and flexible toolkit for building Web APIs.
- PostgreSQL: The database management system used for storing elevator and request data.
- Other dependencies specified in the `requirements.txt` file.

## Future Versions

Here are some ideas for future versions of the Elevator System that we may consider implementing:

- **Weight Consideration**: Include weight as a factor in elevator operations. This can involve tracking the weight of users and ensuring that the elevator does not exceed its weight capacity.
- **External Lift Call Management**: Utilize Redis or a similar caching mechanism to manage external lift calls. This can improve performance and efficiency by optimizing the handling of multiple requests from users on different floors.
- **Enhanced User Interface**: Improve the user interface by adding separate "Up" and "Down" buttons for requesting the lift instead of a single button. This can provide more intuitive control and simplify the user experience.
- **Advanced Scheduling Algorithms**: Implement advanced scheduling algorithms to optimize elevator movement and minimize waiting times for users. This can involve considering factors such as user waiting time, elevator load balancing, and energy efficiency.
- **Real-Time Status Updates**: Develop real-time status updates to provide users with accurate information on elevator availability, estimated arrival times, and current floor positions.
- **Request ID-based Logging**: Implement a logging system with request ID-based logging for production-level debugging. This can help track and analyze the flow of requests, making it easier to troubleshoot and diagnose issues.
- **Authentication Middleware**: Integrate an authentication middleware to secure the API endpoints. This can include authentication mechanisms like token-based authentication or OAuth to ensure that only authorized users can access the elevator system.
- **Fault Tolerance and Redundancy**: Implement fault tolerance and redundancy measures to handle system failures gracefully. This can involve mechanisms such as backup servers, failover systems, and data replication to ensure high availability.

## Conclusion

The Elevator System is a Django-based project that simulates an elevator system with various functionalities. It provides a RESTful API interface to interact with elevators, manage requests, and handle elevator operations.

For more details, please refer to the inline code comments and documentation provided within the project files.
