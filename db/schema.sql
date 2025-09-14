-- products
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT
);

-- properties
CREATE TABLE properties (
    id SERIAL PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    address TEXT,
    timezone VARCHAR(50)
);

-- property_products
CREATE TABLE property_products (
    property_id INT REFERENCES properties(id) ON DELETE CASCADE,
    product_id INT REFERENCES products(id) ON DELETE CASCADE,
    PRIMARY KEY (property_id, product_id)
);

-- property_employees
CREATE TABLE property_employees (
    id SERIAL PRIMARY KEY,
    property_id INT REFERENCES properties(id) ON DELETE CASCADE,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    phone VARCHAR(20),
    role_in_property VARCHAR(50)
);

-- hrs_employees
CREATE TABLE hrs_employees (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    phone VARCHAR(20),
    is_admin BOOLEAN DEFAULT FALSE,
    job_title VARCHAR(100),
    product_id INT REFERENCES products(id)
);

-- support_levels
CREATE TABLE support_levels (
    id SERIAL PRIMARY KEY,
    code VARCHAR(10) UNIQUE NOT NULL,
    description VARCHAR(100) NOT NULL
);

-- duty_roster
CREATE TABLE duty_roster (
    id SERIAL PRIMARY KEY,
    duty_date DATE NOT NULL,
    product_id INT REFERENCES products(id) ON DELETE CASCADE,
    support_level_id INT REFERENCES support_levels(id) ON DELETE CASCADE,
    hrs_employee_id INT REFERENCES hrs_employees(id) ON DELETE CASCADE
);

-- tickets
CREATE TABLE tickets (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    status VARCHAR(30) NOT NULL DEFAULT 'OPEN',
    priority VARCHAR(20) NOT NULL,
    property_id INT REFERENCES properties(id) ON DELETE CASCADE,
    product_id INT REFERENCES products(id) ON DELETE CASCADE,
    created_by_employee_id INT REFERENCES property_employees(id) ON DELETE SET NULL,
    assigned_to_employee_id INT REFERENCES hrs_employees(id) ON DELETE SET NULL,
    support_level_id INT REFERENCES support_levels(id),
    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now(),
    closed_at TIMESTAMP,
    resolution_summary TEXT
);
