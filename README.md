# Coupon Reseller

<!-- [![Django CI](https://github.com/companyname/projectname/actions/workflows/django.yml/badge.svg)](https://github.com/companyname/projectname/actions/workflows/django.yml) -->

Coupon Reseller is built using [Django Web Framework].

[django web framework]: https://www.djangoproject.com/

## Description

This project is designed to let students of NIT Durgapur post ads for selling their unused meal coupons.

To make sure every user is actually a student of the college, registering with institute email address is necessary. Their email ID will be verified by an autogenerated verification email sent to their institution email ID.

Once registered, they will be asked to make a profile,without which they can neither post anything, nor view others' profiles.

A SQLite file containing the Registration Number and corresponding names of the students(currently, only those of UG program) has been prepared in the account directory. If the user registration number exists in the database then their "Name" field in their profile will be autofilled and be immutable by the user. They will  also be marked Verified. The links to their profiles will be shown in green, while the other accounts will be coloured red.

Every user has the ability to edit the posted ads after posting it.



## Requirements

-   Python 3.6+.

## Installation

```bash
# Clone the repo
git clone https://github.com/arin17bishwa/Coupon_Reseller.git
cd Coupon_Reseller

# Set up a virtual environment (.venv is the virtual environment name)
python -m venv .venv
source .venv/bin/activate

# Install the requirements
pip install -r requirements.txt

# Change to project directory
cd src

# Run the migrations
python manage.py makemigrations
python manage.py migrate
```

## Development

You can start the Django development server by activating the virtual
environment and using the `runserver` command:

```bash
source .venv/bin/activate

python manage.py runserver
```


Then open up your browser and go to

```http request
http://127.0.0.1:8000/
```

## Demo

A demo has been put up at [Heroku](https://coupon-reseller.herokuapp.com/).


