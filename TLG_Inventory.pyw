import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import os
import sys
from datetime import datetime
import json
from PIL import Image, ImageTk  # You'll need to pip install pillow
import webbrowser  # Added import
import requests
from tkinter import messagebox
import webbrowser

APP_VERSION = "1.0.0"

def load_config(config_path=None):
    """
    Load configuration from a JSON file.
    If no config_path is provided, looks for config.json in the same directory as the script.
    Returns a dictionary with the config or default values.
    """
    # Default configuration
    default_config = {
        "field_mapping": {
            "erp_item_field": "Item_Number",
            "woo_sku_field": "SKU"
        },
        "excluded_vendors": [
            "UPC CODES",
            "HECTOR CHIN"
        ],
        "excluded_categories": [
            "PARTS",
            "SHIPPING"
        ],
        "category_mapping": {
            "TREES": "Starlit Forest Trees",
            "FOAM FLOWE": "Foam Flowers and Greenery",
            "CANDLE ACC": "Hurricanes and Candle Accessories",
            "MISC": "Home Accents",
            "WALL DECOR": "Wall Decor",
            "VASES": "Vases",
            "LANTERNS": "Lanterns & Chandeliers",
            "RADIANCE": "Radiance LED Candles",
            "PARTS": "Parts",
            "ILLUMINATE": "Illuminated Branches & Trees",
            "SHELL LAMP": "Lighting Features",
            "MARINE": "Coastal Living",
            "BULBS": "LED Bulbs",
            "TABLE TOP": "Occasion Collection Table Lamps & Bottle Toppers",
            "FLAME WAVE": "Flame Illusion Modules & Accessories",
            "SHIPPING": "Shipping",
            "DISCONTINU": "Discontinued",
            "ANIMALS": "Avian Beauties",
            "#N/A": "Uncategorized",
            "SPRAYS": "Decorative Sprays"
        },
        "woo_columns": [
            "SKU", "Name", "Visibility in catalog", "Categories", "Regular Price",
            "Sale price", "Date sale price starts", "Date sale price ends", "Stock",
            "In stock?", "Backorders allowed?", "Type", "Published",
            "Meta: minimum_allowed_quantity", "Meta: group_of_quantity",
            "Meta: minmax_do_not_count", "Meta: minmax_cart_exclude",
            "Meta: minmax_category_group_of_exclude", "Description", "Tax status"
        ],
        "file_names": {
            "new_items_pattern": "NEW_Items_{timestamp}.csv",
            "update_items_pattern": "UPDATE_Items_{timestamp}.csv"
        }
    }
    
    # Determine application path based on whether it's run as a script or frozen exe
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    else:
        application_path = os.path.dirname(os.path.abspath(__file__))
    
    # If no config path provided, use default location
    if config_path is None:
        config_path = os.path.join(application_path, "config.json")
    
    # Try to load the config file
    config = default_config.copy()
    try:
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                loaded_config = json.load(f)
                
            # Update config with loaded values
            # This preserves default values for any missing keys
            for key, value in loaded_config.items():
                if key in config:
                    if isinstance(config[key], dict) and isinstance(value, dict):
                        config[key].update(value)
                    else:
                        config[key] = value
            
            return config
        else:
            # If config file doesn't exist, create a default one
            with open(config_path, 'w') as f:
                json.dump(default_config, f, indent=4)
            print(f"Created default config file at {config_path}")
            return default_config
            
    except Exception as e:
        print(f"Error loading config: {str(e)}")
        print(f"Using default configuration instead")
        return default_config


class CombinedERPWooTool:
    def __init__(self, master):
        self.master = master
        master.title(f"ERP/WooCommerce Import Builder - Version {APP_VERSION}")
        master.geometry("700x650")  # Increased height to accommodate logo header
        
        # Load configuration
        self.config = load_config()
        
        # Set styles
        self.style = ttk.Style()
        self.style.configure("TButton", padding=6, font=('Segoe UI', 10))
        self.style.configure("TLabel", font=('Segoe UI', 10))
        self.style.configure("Accent.TButton", font=("Arial", 11, "bold"))
        
        # Get data from config
        self.CATEGORY_MAPPING = self.config["category_mapping"]
        self.EXCLUDED_VENDORS = set(self.config["excluded_vendors"])
        self.EXCLUDED_CATEGORIES = set(self.config["excluded_categories"])
        self.WOO_COLUMNS = self.config["woo_columns"]
        
        # Variables
        self.erp_path = tk.StringVar()
        self.woo_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.status_var = tk.StringVar()
        self.status_var.set("Ready to begin. Select input files.")
        
        # Field mapping variables from config
        self.erp_item_field = tk.StringVar(value=self.config["field_mapping"]["erp_item_field"])
        self.woo_sku_field = tk.StringVar(value=self.config["field_mapping"]["woo_sku_field"])
        
        # Create the UI
        self.create_widgets()
        
        # Add config menu
        self.create_menu()

    def get_application_path(self):
        """Determine the application path based on whether the script is frozen or not."""
        if getattr(sys, 'frozen', False):
            return os.path.dirname(sys.executable)
        return os.path.dirname(os.path.abspath(__file__))

    def create_widgets(self):
        # Logo header
        self.header_frame = ttk.Frame(self.master)
        self.header_frame.pack(fill=tk.X, pady=10)

        # Load and display logo
        try:
            # Determine application path
            if getattr(sys, 'frozen', False):
                application_path = os.path.dirname(sys.executable)
            else:
                application_path = os.path.dirname(os.path.abspath(__file__))

            logo_path = os.path.join(application_path, "logo.png")

            if os.path.exists(logo_path):
                # Open and resize the logo image
                logo_image = Image.open(logo_path)
                logo_image = logo_image.resize((200, 80), Image.LANCZOS)
                self.logo_photo = ImageTk.PhotoImage(logo_image)

                # Display the logo
                self.logo_label = ttk.Label(self.header_frame, image=self.logo_photo)
                self.logo_label.pack(side=tk.LEFT, padx=20)

                # Add title next to the logo
                self.title_label = ttk.Label(
                    self.header_frame,
                    text="ERP to WooCommerce Tool",
                    font=("Segoe UI", 16, "bold")
                )
                self.title_label.pack(side=tk.LEFT, padx=20)
            else:
                raise FileNotFoundError(f"Logo not found at {logo_path}")

        except Exception as e:
            print(f"Error loading logo: {e}")
            # Fallback to text-only header
            self.title_label = ttk.Label(
                self.header_frame,
                text="ERP to WooCommerce Tool",
                font=("Segoe UI", 18, "bold")
            )
            self.title_label.pack(side=tk.LEFT, padx=20)

        # Main frame
        self.main_frame = ttk.Frame(self.master, padding="20 20 20 20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # File selection frame
        self.file_frame = ttk.LabelFrame(self.main_frame, text="Select Files", padding="10 10 10 10")
        self.file_frame.pack(fill=tk.X, pady=10)

        # ERP file selection
        self.erp_frame = ttk.Frame(self.file_frame)
        self.erp_frame.pack(fill=tk.X, pady=5)

        self.erp_label = ttk.Label(self.erp_frame, text="ERP CSV:        ")
        self.erp_label.pack(side=tk.LEFT, padx=5)

        self.erp_entry = ttk.Entry(self.erp_frame, textvariable=self.erp_path, width=40)
        self.erp_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        self.erp_button = ttk.Button(self.erp_frame, text="Browse...", command=self.select_erp_file)
        self.erp_button.pack(side=tk.LEFT, padx=5)

        # WooCommerce file selection
        self.woo_frame = ttk.Frame(self.file_frame)
        self.woo_frame.pack(fill=tk.X, pady=5)

        self.woo_label = ttk.Label(self.woo_frame, text="WooCommerce CSV:")
        self.woo_label.pack(side=tk.LEFT, padx=5)

        self.woo_entry = ttk.Entry(self.woo_frame, textvariable=self.woo_path, width=40)
        self.woo_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        self.woo_button = ttk.Button(self.woo_frame, text="Browse...", command=self.select_woo_file)
        self.woo_button.pack(side=tk.LEFT, padx=5)

        # Output directory selection
        self.output_frame = ttk.Frame(self.file_frame)
        self.output_frame.pack(fill=tk.X, pady=5)

        self.output_label = ttk.Label(self.output_frame, text="Output Folder:")
        self.output_label.pack(side=tk.LEFT, padx=5)

        self.output_entry = ttk.Entry(self.output_frame, textvariable=self.output_path, width=40)
        self.output_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        self.output_button = ttk.Button(self.output_frame, text="Browse...", command=self.select_output_dir)
        self.output_button.pack(side=tk.LEFT, padx=5)

        # Field mapping frame
        self.mapping_frame = ttk.LabelFrame(self.main_frame, text="Field Mapping", padding="10 10 10 10")
        self.mapping_frame.pack(fill=tk.X, pady=10)

        # SKU field mapping
        self.sku_frame = ttk.Frame(self.mapping_frame)
        self.sku_frame.pack(fill=tk.X, pady=5)

        self.woo_sku_label = ttk.Label(self.sku_frame, text="WooCommerce SKU field:")
        self.woo_sku_label.pack(side=tk.LEFT, padx=5)

        self.woo_sku_entry = ttk.Entry(self.sku_frame, textvariable=self.woo_sku_field, width=20)
        self.woo_sku_entry.pack(side=tk.LEFT, padx=5)

        self.erp_item_label = ttk.Label(self.sku_frame, text="ERP Item Number field:")
        self.erp_item_label.pack(side=tk.LEFT, padx=5)

        self.erp_item_entry = ttk.Entry(self.sku_frame, textvariable=self.erp_item_field, width=20)
        self.erp_item_entry.pack(side=tk.LEFT, padx=5)

        # View mappings button
        self.mapping_button = ttk.Button(self.mapping_frame, text="View Category Mappings", command=self.show_category_mappings)
        self.mapping_button.pack(fill=tk.X, pady=5)

        # Action buttons
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(fill=tk.X, pady=20)

        self.process_button = ttk.Button(
            self.button_frame,
            text="Process Files",
            command=self.process_files,
            style="Accent.TButton"
        )
        self.process_button.pack(side=tk.LEFT, padx=5)

        self.exit_button = ttk.Button(self.button_frame, text="Exit", command=self.master.quit)
        self.exit_button.pack(side=tk.RIGHT, padx=5)

        # Status bar
        self.status_bar = ttk.Label(self.master, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Progress bar
        self.progress = ttk.Progressbar(self.main_frame, orient=tk.HORIZONTAL, length=100, mode='determinate')
        self.progress.pack(fill=tk.X, pady=10)
    
    def create_menu(self):
        """Create a menu bar with configuration options"""
        self.menu_bar = tk.Menu(self.master)
        self.master.config(menu=self.menu_bar)
        
        # File menu
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Exit", command=self.master.quit)
        
        # Configuration menu
        config_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Configuration", menu=config_menu)
        config_menu.add_command(label="Edit Configuration", command=self.edit_config)
        config_menu.add_command(label="Reload Configuration", command=self.reload_config)
        
        # Help menu
        help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Documentation", command=self.open_documentation)  # Added
        help_menu.add_command(label="About", command=self.show_about)
        help_menu.add_command(label="Check for Updates", command=check_for_update)  # Added
    
    def edit_config(self):
        """Open the config file in the default text editor, creating it if necessary."""
        try:
            if getattr(sys, 'frozen', False):
                application_path = os.path.dirname(sys.executable)
            else:
                application_path = os.path.dirname(os.path.abspath(__file__))
            
            config_path = os.path.join(application_path, "config.json")
            
            # Always ensure config file exists
            if not os.path.exists(config_path):
                default_config = load_config()  # Load will create if missing
                with open(config_path, 'w') as f:
                    json.dump(default_config, f, indent=4)
            
            # Open config in editor
            if sys.platform == 'win32':
                os.startfile(config_path)
            elif sys.platform == 'darwin':  # macOS
                os.system(f'open "{config_path}"')
            else:  # Linux
                os.system(f'xdg-open "{config_path}"')
            
            self.status_var.set("Opened configuration file for editing")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open config file: {str(e)}")
    
    def reload_config(self):
        """Reload the configuration file"""
        try:
            self.config = load_config()
            
            # Update variables from config
            self.CATEGORY_MAPPING = self.config["category_mapping"]
            self.EXCLUDED_VENDORS = set(self.config["excluded_vendors"])
            self.EXCLUDED_CATEGORIES = set(self.config["excluded_categories"])
            self.WOO_COLUMNS = self.config["woo_columns"]
            
            # Update field mapping variables
            self.erp_item_field.set(self.config["field_mapping"]["erp_item_field"])
            self.woo_sku_field.set(self.config["field_mapping"]["woo_sku_field"])
            
            self.status_var.set("Configuration reloaded successfully")
            messagebox.showinfo("Configuration Reloaded", "Configuration has been reloaded successfully.")
        except Exception as e:
            self.status_var.set(f"Error reloading configuration: {str(e)}")
            messagebox.showerror("Error", f"Failed to reload configuration: {str(e)}")
    
    def show_about(self):
        """Show the about dialog"""
        about_text = f"""ERP/WooCommerce Import Builder

A tool to convert ERP data to WooCommerce import format,
identifying new and updated products automatically.

Version: {APP_VERSION}

This application uses a config.json file for customization.
"""
        messagebox.showinfo("About", about_text)
    
    def open_documentation(self):
        """Open the documentation in the default web browser"""
        documentation_url = "https://example.com/documentation"  # Replace with actual URL
        webbrowser.open(documentation_url)
            
    def select_erp_file(self):
        filepath = filedialog.askopenfilename(
            title="Select ERP CSV",
            filetypes=(("CSV files", "*.csv"), ("All files", "*.*"))
        )
        if filepath:
            self.erp_path.set(filepath)
            self.status_var.set(f"ERP file selected: {os.path.basename(filepath)}")
            
    def select_woo_file(self):
        filepath = filedialog.askopenfilename(
            title="Select WooCommerce CSV",
            filetypes=(("CSV files", "*.csv"), ("All files", "*.*"))
        )
        if filepath:
            self.woo_path.set(filepath)
            self.status_var.set(f"WooCommerce file selected: {os.path.basename(filepath)}")
            
    def select_output_dir(self):
        dirpath = filedialog.askdirectory(title="Select Output Directory")
        if dirpath:
            self.output_path.set(dirpath)
            self.status_var.set(f"Output directory selected: {os.path.basename(dirpath)}")
            
    def show_category_mappings(self):
        # Create a new window to display the category mappings
        mapping_window = tk.Toplevel(self.master)
        mapping_window.title("Category Mappings")
        mapping_window.geometry("600x400")
        mapping_window.transient(self.master)
        mapping_window.grab_set()
        
        # Create a frame for the mappings
        frame = ttk.Frame(mapping_window, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Add a scrollbar
        scrollbar = ttk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create a treeview to display the mappings
        tree = ttk.Treeview(frame, columns=("ERP Category", "WooCommerce Category"), 
                           show="headings", yscrollcommand=scrollbar.set)
        scrollbar.config(command=tree.yview)
        
        # Set column headings
        tree.heading("ERP Category", text="ERP Item_Class")
        tree.heading("WooCommerce Category", text="WooCommerce Category")
        
        # Set column widths
        tree.column("ERP Category", width=150)
        tree.column("WooCommerce Category", width=350)
        
        # Add the mappings to the treeview
        for erp_cat, woo_cat in self.CATEGORY_MAPPING.items():
            tree.insert("", "end", values=(erp_cat, woo_cat))
        
        tree.pack(fill=tk.BOTH, expand=True)
        
        # Add a close button
        close_button = ttk.Button(mapping_window, text="Close", command=mapping_window.destroy)
        close_button.pack(pady=10)
            
    def process_files(self):
        # Validate inputs
        if not self.erp_path.get():
            messagebox.showerror("Error", "Please select an ERP CSV file")
            return
            
        if not self.woo_path.get():
            messagebox.showerror("Error", "Please select a WooCommerce CSV file")
            return
            
        if not self.output_path.get():
            messagebox.showerror("Error", "Please select an output directory")
            return
            
        try:
            self.status_var.set("Loading ERP data...")
            self.master.update_idletasks()
            self.progress['value'] = 10
            
            # Load ERP CSV
            erp_df = pd.read_csv(self.erp_path.get())
            
            # Get field names
            erp_item_field = self.erp_item_field.get()
            
            # Validate ERP field names
            if erp_item_field not in erp_df.columns:
                messagebox.showerror("Error", f"Field '{erp_item_field}' not found in ERP CSV")
                return
                
            self.status_var.set("Cleaning ERP data...")
            self.master.update_idletasks()
            self.progress['value'] = 20
            
            # Clean ERP data
            # Filter out vendors to exclude
            if "Vendor_Name" in erp_df.columns:
                erp_df = erp_df[~erp_df["Vendor_Name"].str.upper().isin(self.EXCLUDED_VENDORS)]
            
            # Filter out "Added using Check Links" description
            if "Description" in erp_df.columns:
                erp_df = erp_df[erp_df["Description"].str.strip() != "Added using Check Links"]
            
            # Filter out excluded categories
            if "Item_Class" in erp_df.columns:
                erp_df = erp_df[~erp_df["Item_Class"].isin(self.EXCLUDED_CATEGORIES)]
            
            # Verify required columns exist in ERP data
            required_columns = [
                erp_item_field, "Description", "Item_Status", "List_Price", 
                "Quantity_On_Hand", "Minimum_Order_Qty", "Item_Notes", "Item_Class"
            ]

            missing_columns = [col for col in required_columns if col not in erp_df.columns]
            if missing_columns:
                missing_cols_str = ", ".join(missing_columns)
                messagebox.showerror("Error", f"Missing required columns in ERP CSV: {missing_cols_str}")
                self.status_var.set(f"Error: Missing required columns: {missing_cols_str}")
                return
            
            self.status_var.set("Loading WooCommerce data...")
            self.master.update_idletasks()
            self.progress['value'] = 30
            
            # Load WooCommerce CSV
            woo_df = pd.read_csv(self.woo_path.get())
            
            # Get WooCommerce field name
            woo_sku_field = self.woo_sku_field.get()
            
            # Validate WooCommerce field name
            if woo_sku_field not in woo_df.columns:
                messagebox.showerror("Error", f"Field '{woo_sku_field}' not found in WooCommerce CSV")
                return
                
            self.status_var.set("Comparing ERP and WooCommerce data...")
            self.master.update_idletasks()
            self.progress['value'] = 40
            
            # Get list of SKUs from WooCommerce
            woo_skus = set(woo_df[woo_sku_field].astype(str))
            
            # Split ERP items based on existence in WooCommerce
            new_items = erp_df[~erp_df[erp_item_field].astype(str).isin(woo_skus)]
            update_items = erp_df[erp_df[erp_item_field].astype(str).isin(woo_skus)]
            
            # Generate timestamp for filenames
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Get filename patterns from config
            new_items_pattern = self.config["file_names"]["new_items_pattern"]
            update_items_pattern = self.config["file_names"]["update_items_pattern"]
            
            # Format with timestamp
            new_items_filename = new_items_pattern.format(timestamp=timestamp)
            update_items_filename = update_items_pattern.format(timestamp=timestamp)
            
            # Build output paths
            output_dir = self.output_path.get()
            new_file_path = os.path.join(output_dir, new_items_filename)
            update_file_path = os.path.join(output_dir, update_items_filename)
            
            # Track what files were created
            files_created = []
            
            # Process new items if any exist
            if len(new_items) > 0:
                self.status_var.set(f"Converting {len(new_items)} new items...")
                self.master.update_idletasks()
                self.progress['value'] = 60
                
                # Create WooCommerce import file for new items
                new_woo_df = self.convert_to_woo_format(new_items, erp_item_field)
                
                # Save new items file
                new_woo_df.to_csv(new_file_path, index=False)
                files_created.append(("New items", new_file_path, len(new_items)))
            
            # Process update items if any exist
            if len(update_items) > 0:
                self.status_var.set(f"Converting {len(update_items)} update items...")
                self.master.update_idletasks()
                self.progress['value'] = 80
                
                # Create WooCommerce import file for update items
                update_woo_df = self.convert_to_woo_format(update_items, erp_item_field)
                
                # Save update items file
                update_woo_df.to_csv(update_file_path, index=False)
                files_created.append(("Update items", update_file_path, len(update_items)))
            
            self.progress['value'] = 100
            
            # Show completion message with stats
            if len(files_created) > 0:
                msg = "Processing complete!\n\n"
                msg += f"Total ERP items analyzed: {len(erp_df)}\n\n"
                
                for file_type, path, count in files_created:
                    msg += f"{file_type}: {count}\n"
                    msg += f"File: {os.path.basename(path)}\n\n"
                
                if len(new_items) == 0:
                    msg += "No new items found - no NEW file created.\n\n"
                    
                if len(update_items) == 0:
                    msg += "No items to update - no UPDATE file created.\n\n"
                
                msg += "Next steps:\n"
                if len(new_items) > 0:
                    msg += "- Import NEW items file in WooCommerce\n"
                if len(update_items) > 0:
                    msg += "- Import UPDATE items file in WooCommerce\n"
                
                messagebox.showinfo("Complete", msg)
                self.status_var.set(f"Ready - Processed {len(erp_df)} items")
            else:
                messagebox.showinfo("Complete", "No files were created. No new or update items found.")
                self.status_var.set("Ready - No files created")
            
        except Exception as e:
            self.progress['value'] = 0
            self.status_var.set("Error encountered")
            messagebox.showerror("Error", str(e))
    
    def convert_to_woo_format(self, erp_df, erp_item_field):
        """Convert ERP dataframe to WooCommerce import format"""
        
        # Get WooCommerce columns from config
        woo_columns = self.WOO_COLUMNS
        
        # Create empty DataFrame with WooCommerce columns
        df_woo = pd.DataFrame(columns=woo_columns)
        
        # Map fields from ERP to WooCommerce
        df_woo["SKU"] = erp_df[erp_item_field]
        df_woo["Name"] = erp_df["Description"]
        
        # Map visibility based on Item_Status
        df_woo["Visibility in catalog"] = erp_df["Item_Status"].apply(
            lambda x: "hidden" if x in ["Active", "Discontinued"] else "visible"
        )
        
        # Map Categories using the mapping dictionary
        df_woo["Categories"] = erp_df["Item_Class"].apply(
            lambda x: self.CATEGORY_MAPPING.get(x, "Uncategorized") if pd.notna(x) else "Uncategorized"
        )
        
        df_woo["Regular Price"] = erp_df["List_Price"]
        df_woo["Stock"] = erp_df["Quantity_On_Hand"]
        df_woo["Meta: minimum_allowed_quantity"] = erp_df["Minimum_Order_Qty"]
        df_woo["Description"] = erp_df["Item_Notes"]
        df_woo["Meta: group_of_quantity"] = erp_df["Minimum_Order_Qty"]
        
        # Handle DISCONTINUED items
        discontinued_mask = erp_df["Item_Class"] == "DISCONTINU"
        df_woo.loc[discontinued_mask, "Stock"] = 0
        df_woo.loc[discontinued_mask, "Visibility in catalog"] = "hidden"
        
        # Set static values
        df_woo["Type"] = "simple"
        df_woo["Published"] = 1
        df_woo["Date sale price starts"] = ""  # Leave blank
        df_woo["Date sale price ends"] = ""    # Leave blank
        df_woo["Tax status"] = "taxable"
        df_woo["Sale price"] = ""  # Leave blank
        
        # Set "In stock?" based on stock level
        df_woo["In stock?"] = erp_df["Quantity_On_Hand"].apply(
            lambda x: "no" if x == 0 else "yes"
        )
        
        df_woo["Backorders allowed?"] = 1
        df_woo["Meta: minmax_do_not_count"] = "no"
        df_woo["Meta: minmax_cart_exclude"] = "no"
        df_woo["Meta: minmax_category_group_of_exclude"] = "no"
        
        # Ensure all columns exist before returning
        for col in woo_columns:
            if col not in df_woo.columns:
                df_woo[col] = ""
                
        # Return sorted dataframe
        return df_woo[woo_columns]


def check_for_update():
    """Check for software updates by comparing the current version with the latest version."""
    try:
        # Hosted version.txt and EXE download links
        version_url = "https://drive.google.com/uc?export=download&id=17qdLhSYD0RrFEz0_yz8vknUxS3HJIWbe"
        exe_download_url = "https://drive.google.com/uc?export=download&id=1sO7a_m9w8xlHYtMkMngxW3L2Fb-5nCkP"
        
        response = requests.get(version_url, timeout=5)
        if response.status_code == 200:
            latest_version = response.text.strip()
            if latest_version != APP_VERSION:
                answer = messagebox.askyesno(
                    "Update Available - The Marketing Systems Collective",
                    f"A newer version ({latest_version}) of this software is available.\n\n"
                    "Would you like to download the latest version now?"
                )
                if answer:
                    webbrowser.open(exe_download_url)
            else:
                print("No update needed. Running latest version.")
        else:
            print("Failed to check for update.")

    except Exception as e:
        print(f"Update check failed: {e}")


def main():
    root = tk.Tk()
    app = CombinedERPWooTool(root)
    root.mainloop()
    
if __name__ == "__main__":
    main()