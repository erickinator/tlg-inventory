ERP to WooCommerce Import Tool
Developed by The Marketing Systems Collective

Overview
This application bridges the gap between Great Plains ERP and WooCommerce by handling the product synchronization process. It solves a key limitation in WooCommerce's native import system, which requires separate imports for new and updated products.

What It Does
The application:

Takes an ERP CSV export and a WooCommerce product export as inputs
Cleans and filters the ERP data based on configurable rules
Determines which products are new vs. which need updates
Converts the ERP data format to WooCommerce's expected format
Creates separate import files for new and updated products
Provides clear next steps for importing these files into WooCommerce
System Requirements
Python 3.6 or higher
Required Python packages:
pandas
pillow (for logo display)
Optional: logo.png file in the same directory as the application
Configuration
The application uses a config.json file for all settings. This file is automatically created on first run with default values that match your current setup.

Accessing and Editing the Configuration
You can access the configuration in two ways:

From the application: Select "Configuration → Edit Configuration" from the menu. This opens the config file in your default text editor.
Directly: Open the config.json file in any text editor. The file is stored in the same directory as the application.
After editing, select "Configuration → Reload Configuration" in the application to apply your changes.

Configuration Sections
The config file is organized into several sections, each controlling different aspects of the application:

Field Mapping
{
  "field_mapping": {
    "erp_item_field": "Item_Number",
    "woo_sku_field": "SKU"
  }
}
This section defines which fields in your CSV files contain the unique identifiers for products. These fields are used to match products between ERP and WooCommerce.

When to customize: If your ERP export uses different column names for item numbers, or if your WooCommerce export uses a different field for SKUs.

Excluded Vendors and Categories
{
  "excluded_vendors": [
    "UPC CODES",
    "HECTOR CHIN"
  ],
  "excluded_categories": [
    "PARTS",
    "SHIPPING"
  ]
}
These sections control which records are filtered out of the ERP data before processing.

When to customize:

Add vendor names to exclude certain suppliers from being imported
Add category names to exclude entire product categories from processing
Category Mapping
{
  "category_mapping": {
    "TREES": "Starlit Forest Trees",
    "FOAM FLOWE": "Foam Flowers and Greenery",
    ...
  }
}
This dictionary maps ERP category codes to WooCommerce category names. The keys are the values found in your ERP's "Item_Class" field, and the values are the corresponding WooCommerce category names.

When to customize:

When adding new product categories in ERP
When changing WooCommerce category names
When reorganizing your WooCommerce category structure
WooCommerce Columns
{
  "woo_columns": [
    "SKU", "Name", "Visibility in catalog", 
    ...
  ]
}
This section defines which columns will be included in the output files and in what order.

When to customize: If you need to add or remove fields for WooCommerce imports, or change the order of columns in the output files.

File Name Patterns
{
  "file_names": {
    "new_items_pattern": "NEW_Items_{timestamp}.csv",
    "update_items_pattern": "UPDATE_Items_{timestamp}.csv"
  }
}
This section controls the naming pattern for output files. The {timestamp} placeholder is automatically replaced with the current date and time when files are created.

When to customize: If you prefer different naming conventions for output files.

How Field Mapping Works
The application doesn't just copy data from ERP to WooCommerce - it transforms it according to WooCommerce's needs:

Core Field Transformations
Product Identification: ERP Item Numbers become WooCommerce SKUs
Product Naming: ERP Descriptions become WooCommerce product Names
Categorization: ERP Item Classes are mapped to WooCommerce Categories using the category mapping dictionary
Pricing: ERP List Prices become WooCommerce Regular Prices
Inventory: ERP Quantity on Hand becomes WooCommerce Stock and determines In-stock status
Details: ERP Item Notes become WooCommerce product Descriptions
Order Quantities: ERP Minimum Order Quantities are mapped to WooCommerce meta fields that control minimum purchase quantities
Special Handling
Visibility Logic: Products with certain Item Status values (like "Active" or "Discontinued") are set to hidden in WooCommerce
Discontinued Products: Products in the "DISCONTINU" category have their stock set to zero and visibility set to hidden
Minimum Purchase Rules: The ERP minimum order quantity is used for both the minimum allowed quantity and the quantity increment step
Default Values
Many WooCommerce fields that don't have a direct ERP equivalent are set to sensible defaults:

Product type is set to "simple"
Products are published by default
Tax status is set to "taxable"
Backorders are allowed
Various min/max quantity plugin settings are configured
Data Filtering Process
Before comparing products and creating import files, the application cleans the ERP data:

Vendor Filtering: Removes products from specified vendors (e.g., placeholder vendors like "UPC CODES")
Description Filtering: Removes products with specific descriptions that indicate they shouldn't be imported
Category Filtering: Removes products in categories that shouldn't be synchronized with WooCommerce
This filtering ensures that only relevant products are processed and imported to WooCommerce.

How Product Comparison Works
The application determines whether products are new or updates by:

Loading your WooCommerce export and extracting all existing SKUs
Comparing each ERP item number against this list of SKUs
Classifying items as:
New: If the ERP item number doesn't exist as a SKU in WooCommerce
Update: If the ERP item number already exists as a SKU in WooCommerce
This comparison happens after filtering, so the numbers shown in the completion message reflect only the products that passed all filters.

Usage Workflow
Initial Setup
Run the application for the first time
If needed, use "Configuration → Edit Configuration" to customize settings
Add a logo.png file to the application directory if desired
Regular Use
Export your current products from WooCommerce
Export your product data from Great Plains ERP
In the application:
Select the ERP CSV file
Select the WooCommerce export file
Choose where to save the output files
Click "Process Files"
Import the resulting files into WooCommerce:
Import the NEW_Items file first (if created)
Import the UPDATE_Items file second (if created)
Handling Changes
If your business requirements change:

New Categories: Edit the category_mapping section in config.json
Different Vendors to Exclude: Edit the excluded_vendors section
New File Naming Conventions: Edit the file_names section
Field Name Changes: Edit the field_mapping section
After any change to the configuration, use "Reload Configuration" in the application before processing files.

Troubleshooting
Common issues:

"Field not found" error: Check that your CSV column names match the expected field names in the configuration
No files created: Ensure your ERP and WooCommerce exports contain data and the SKU fields are correctly mapped
Empty data after import: Verify all required fields are present in your ERP export
Key Points to Remember
The application filters data before determining new vs. update status
The numbers in the completion message reflect products after filtering
All mapping and filtering rules can be customized in the config.json file
Always reload the configuration after making changes
Support
For questions or issues, please contact The Marketing Systems Collective.

Documentation created for ERP to WooCommerce Import Tool, explicitly for The Light Garden

© The Marketing Systems Collective