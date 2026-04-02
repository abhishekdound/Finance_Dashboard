Finance Dashboard Backend:
 
    A robust, modular FastAPI backend designed for financial data management. This system features Role-Based Access Control (RBAC), real-time dashboard analytics, and secure JWT authentication.


Key Features:


    User & Role Management: Three distinct tiers: Admin (Full access), Analyst (Read + Analytics), and Viewer (Read-only).
    
    Financial CRUD: Full Create, Read, Update, and Delete operations for income and expense records.
    
    Live Analytics: Aggregated dashboard summaries including Total Income, Total Expenses, Net Balance, and Category-wise breakdowns.
    
    Security First: Password hashing with Bcrypt and secure JWT (JSON Web Token) authentication.
    
    Smart Pagination: High-performance data fetching with total_pages and current_page metadata.
    
    Data Integrity: Strict validation using Pydantic (e.g., non-negative amounts, specific transaction types).

Tech Stack:

    Framework: FastAPI
    ORM: SQLAlchemy 2.0
    Database: SQLite (Relational)
    Validation: Pydantic v2
    Security: Passlib (Bcrypt) & Python-Jose (JWT)
    Package Manager: uv

Project Structure:

    Finance_Dashboard/
    ├── main.py                 # App entry point & CORS config
    ├── seed.py                 # Database initialization & sample users
    ├── app/
    │   ├── api/                # API Endpoints & Dependencies
    │   │   ├── deps.py         # Auth & Role Guards
    │   │   └── endpoints/      # Records, Auth, & Summary routes
    │   ├── core/               # Security & JWT logic
    │   ├── models/             # SQLAlchemy Database Models
    │   ├── schemas/            # Pydantic Validation Schemas
    │   └── database.py         # SQLite Engine & Session setup
    └── database.db              # Local SQLite database file


Configuration (.env):

    Create a .env file in the root directory to store your security credentials:

    SECRET_KEY=your_super_secret_key_here
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    

Installation & Setup:

    Clone the repository:

    git clone <your-repo-url>
    cd Finance_Dashboard
    
    Install dependencies:

    Using uv (recommended for speed):
    uv add fastapi "uvicorn[standard]" sqlalchemy pydantic-settings "python-jose[cryptography]" "passlib[bcrypt]" python-multipart "bcrypt==4.0.1"
    
    
    Seed the Database:

    This creates the required Roles and initial Users (Admin, Analyst, Viewer).
    uv run seed.py
    
    
    Run the Server:

    uv run uvicorn main:app --reload



API Endpoints Reference:

     Authentication:

        Endpoint	            Method	    Description	                                        Auth Required
        /token	                POST	    Exchange credentials for JWT Access Token	        No

     Financial Records:

        Endpoint	            Method	    Description	                                        Min. Role
        /api/v1/records/	    GET	        List all records (Supports Pagination & Filters)	Viewer
        /api/v1/records/	    POST	    Create a new financial entry	                    Admin
        /api/v1/records/{id}	PUT	        Update an existing record	                        Admin
        /api/v1/records/{id}	DELETE	    Remove a record	                                    Admin

     Dashboard & Analytics:

        Endpoint	                Method	    Description	                                        Min. Role
        /api/v1/records/summary	    GET	        Get total income, expenses, and net balance	        Viewer
        /api/v1/records/paginated	GET	        Fetch records with total_pages metadata             Viewer




Accessing the API:

    Documentation:

        Access the interactive Swagger UI at:
             127.0.0.1/Your-Port/docs

    Login Request (Postman/Frontend):

        To get your access token, send a POST request:
        URL: http://127.0.0.1:Your-Port/token
        Body Type: x-www-form-urlencoded
        Payload:
        username: admin@test.com
        password: pass123


    Default Test Credentials:
    
        Role	   Email	            Password    
        Admin	   admin@test.com	    pass123
        Analyst	   analyst@test.com	    pass123
        Viewer	   viewer@test.com	    pass123
