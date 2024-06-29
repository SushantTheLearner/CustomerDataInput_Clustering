import pandas as pd
from sklearn.cluster import KMeans
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

# Function to add a new customer record
def add_customer():
    try:
        # Retrieve input data
        fname = fname_var.get()
        lname = lname_var.get()
        avg_purchase = float(avg_purchase_var.get())
        freq = int(freq_var.get())
        lifespan = int(lifespan_var.get())

        # Create a new customer dictionary
        new_customer = {
            'First Name': fname,
            'Last Name': lname,
            'Average Purchase Value': avg_purchase,
            'Purchase Frequency': freq,
            'Customer Lifespan': lifespan
        }
        
        # Convert to DataFrame and append to CSV
        new_customer_df = pd.DataFrame([new_customer])
        if not os.path.isfile('customer_data.csv'):
            new_customer_df.to_csv('customer_data.csv', index=False)
        else:
            new_customer_df.to_csv('customer_data.csv', mode='a', header=False, index=False)

        # Show success message
        messagebox.showinfo("Success", "Customer added successfully!")

        # Clear input fields
        fname_var.set("")
        lname_var.set("")
        avg_purchase_var.set("")
        freq_var.set("")
        lifespan_var.set("")
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers for purchase value, frequency, and lifespan.")

# Function to perform KMeans clustering on customer data
def run_clustering():
    try:
        # Check for existing data file
        if not os.path.isfile('customer_data.csv') or os.path.getsize('customer_data.csv') == 0:
            messagebox.showerror("Data Error", "No customer data found. Add at least two customers to perform clustering.")
            return
        
        # Read customer data from CSV
        customer_df = pd.read_csv('customer_data.csv')
        print("Loaded customer data:\n", customer_df)  # Debug: Print the entire DataFrame
        
        # Ensure enough data points
        if customer_df.shape[0] < 2:
            messagebox.showerror("Data Error", "At least two customers are needed to perform clustering.")
            return
        
        # Rename columns for consistency
        customer_df.rename(columns={
            'Average Purchase Value': 'AvgPurchase',
            'Purchase Frequency': 'Freq',
            'Customer Lifespan': 'Lifespan'
        }, inplace=True)
        
        # Perform KMeans clustering
        features = customer_df[['AvgPurchase', 'Freq', 'Lifespan']]
        kmeans = KMeans(n_clusters=3, random_state=42).fit(features)
        customer_df['Cluster'] = kmeans.labels_

        # Plot clustering results
        fig, ax = plt.subplots()
        scatter = ax.scatter(customer_df['AvgPurchase'], customer_df['Freq'], c=customer_df['Cluster'], cmap='viridis')
        legend1 = ax.legend(*scatter.legend_elements(), title="Clusters")
        ax.add_artist(legend1)
        plt.xlabel('Average Purchase Value')
        plt.ylabel('Purchase Frequency')
        
        # Display plot in Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().pack()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred during clustering: {e}")

# Function to clear customer data
def clear_customer_data():
    try:
        # Check for existing data file
        if not os.path.isfile('customer_data.csv'):
            messagebox.showerror("File Error", "Customer data file does not exist.")
            return
        
        # Read and check if file is empty
        customer_df = pd.read_csv('customer_data.csv')
        if customer_df.empty:
            messagebox.showinfo("Info", "Customer data file is already empty.")
            return

        # Clear data while retaining headers
        customer_df.iloc[0:0].to_csv('customer_data.csv', index=False)
        messagebox.showinfo("Success", "Customer data cleared successfully!")
    except PermissionError as e:
        messagebox.showerror("Permission Error", f"Permission denied: {e}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Set up the Tkinter GUI
root = Tk()
root.title("Customer Segmentation Tool")
root.geometry("400x500")

# Input fields and labels
Label(root, text="First Name").pack()
fname_var = StringVar()
Entry(root, textvariable=fname_var).pack()

Label(root, text="Last Name").pack()
lname_var = StringVar()
Entry(root, textvariable=lname_var).pack()

Label(root, text="Average Purchase Value").pack()
avg_purchase_var = StringVar()
Entry(root, textvariable=avg_purchase_var).pack()

Label(root, text="Purchase Frequency").pack()
freq_var = StringVar()
Entry(root, textvariable=freq_var).pack()

Label(root, text="Customer Lifespan").pack()
lifespan_var = StringVar()
Entry(root, textvariable=lifespan_var).pack()

# Buttons
Button(root, text="Add Customer", command=add_customer).pack()
Button(root, text="Run Clustering", command=run_clustering).pack()
Button(root, text="Clear Data", command=clear_customer_data).pack()

# Start the Tkinter event loop
root.mainloop()
