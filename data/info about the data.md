# Amazon Sales Report Dataset

## Overview
This dataset contains order information from Amazon's sales platform, specifically Amazon.in. It details various aspects of orders including their status, fulfillment method, product details, and shipping information.

## Column Descriptions

| Column Name | Description |
|-------------|-------------|
| `index` | Numerical index assigned to each row in the dataset |
| `Order ID` | Unique identifier for each order placed on Amazon |
| `Date` | Date when the order was placed (format: MM-DD-YY) |
| `Status` | Current status of the order (e.g., Shipped, Cancelled, Delivered) |
| `Fulfilment` | Entity responsible for fulfilling the order (Merchant or Amazon) |
| `Sales Channel` | Platform where the sale occurred (Amazon.in) |
| `ship-service-level` | Shipping method selected (Standard or Expedited) |
| `Style` | Product style code or identifier |
| `SKU` | Stock Keeping Unit - unique identifier for product including variations |
| `Category` | Product category (e.g., kurta, Set, Western Dress, Top) |
| `Size` | Size of the product (XS, S, M, L, XL, XXL, XXXL, etc.) |
| `ASIN` | Amazon Standard Identification Number - unique product identifier |
| `Courier Status` | Status of shipment with the courier service |
| `Qty` | Quantity of items ordered |
| `currency` | Currency used for the transaction (INR - Indian Rupee) |
| `Amount` | Price of the order in the specified currency |
| `ship-city` | City where the order was shipped to |
| `ship-state` | State/province where the order was shipped to |
| `ship-postal-code` | Postal/ZIP code of the shipping address |
| `ship-country` | Country where the order was shipped to (IN - India) |
| `promotion-ids` | IDs of promotions or offers applied to the order |
| `B2B` | Boolean indicating if the order is a Business-to-Business transaction (True/False) |
| `fulfilled-by` | Service used for order fulfillment (e.g., Easy Ship) |
| `Unnamed: 22` | Empty column with no specific data |

## Notes
- This dataset appears to focus on fashion items (kurtas, dresses, tops, sets)
- Geographic coverage is primarily within India, with orders shipping to various states
- The dataset includes both fulfilled and cancelled orders
- Multiple shipping and fulfillment methods are represented