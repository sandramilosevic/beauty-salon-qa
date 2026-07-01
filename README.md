# Automated Testing of Website Functionality and User Interface

Automated tests for the website **ceragemkrusevac.com**, written in Python using **Pytest** and **Selenium**.

## Overview

This project presents automated testing of the functionality and user interface of the Ceragem cosmetic salon website from Kruševac.  
The goal was to verify whether the most important website features work correctly from the end user’s perspective, including navigation, links, content, SEO elements, and mobile behavior.

The tests are organized to cover realistic user scenarios and detect issues that may affect usability.

## Project Goal

The main goal of this project is to use automated tests to verify:

- navigation menu functionality,
- availability of important links,
- presence of key content,
- basic SEO elements,
- responsiveness on mobile devices.

## Technologies Used

- Python
- Pytest
- Selenium
- ChromeDriver
- Chrome headless mode

## Test Coverage

The project covers the following areas:

- Navigation.
- Links to services and external pages.
- Visibility of key content.
- SEO meta tags.
- Mobile website behavior.

## Implemented Test Classes

### TestNavigacija
Checks whether the navigation menu contains all required items and whether the pages open correctly.

### TestLinkovi
Checks the validity of service links, the Facebook page, and the partner salon website.

### TestSadrzaj
Checks whether the homepage contains an H1 heading, visible images, and whether the gallery contains real images.

### TestSEO
Checks the meta description and robots meta tag.

### TestMobilniPrikaz
Checks the mobile layout of the website, the presence of a hamburger menu, page width, and the visibility of the phone link.

## Key Findings

The testing revealed one issue on the website:

- the **“Call Us”** button exists in the HTML code,
- but it is not visible on the mobile version because of CSS styling.

This problem directly affects user experience because mobile users cannot easily access the contact number from the navigation area.

## Project Structure

```text
├── tests
    ├── test_ceragemkrusevac.py
├── README.md
└── requirements.txt
```

## Installation

Install the required packages:

```bash
pip install pytest selenium
```

You also need:

- Google Chrome,
- a compatible version of ChromeDriver.

## Running Tests

To run all tests, use:

```bash
pytest test_ceragemkrusevac.py -v
```

The `-v` option shows each test individually with its status.

## Example of Detected Issue

One of the tests showed that the phone link exists in the page code, but is not visible on the mobile layout.  
This means that the feature exists technically, but is not available to users through the interface.

<img width="1572" height="367" alt="image" src="https://github.com/user-attachments/assets/ed8dc3c0-b0c5-4562-a0ac-bee451f4ded1" />


## Conclusion

Automated testing proved to be an effective way to verify the website and detect issues that could easily be missed during manual testing.  
The results confirm that Selenium and Pytest can reliably check essential website functionality and mobile behavior.

## License

MIT
