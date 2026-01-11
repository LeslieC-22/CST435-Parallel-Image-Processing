# CST435: Parallel and Cloud Computing – Assignment 2  (Group 20)
## Parallel Image Processing System (Python)


## Project Overview
This project implements a parallel image processing system in Python that applies multiple image filters to a subset of images from the Food-101 dataset. The main objective is to compare different parallel programming approaches in Python and analyse their performance when executed on Google Cloud Platform (GCP).

A sequential (serial) implementation is first developed and used as a baseline for performance evaluation. Two parallel implementations are then developed and compared against this baseline.


## Dataset
https://www.kaggle.com/datasets/dansbecker/food-101

For performance evaluation, only subsets of the dataset were used. Two dataset sizes were selected:
- 100 images for small-scale testing 
- 5000 images for large-scale testing


## Image Processing Operations
1. Grayscale conversion
2. Gaussian blur (3×3 kernel)
3. Edge detection (Sobel filter)
4. Image sharpening
5. Brightness adjustment


## Implementation

### 1. Sequential (Serial) Version
- Implemented in Python
- Processes images one by one
- Uses a single CPU core
- Serves as the baseline for performance comparison

### 2. Parallel - Multiprocessing
- Implemented using Python’s `multiprocessing` module
- Creates separate processes for each worker
- Utilises multiple CPU cores
- Bypasses Python’s Global Interpreter Lock (GIL)
- Suitable for CPU-bound image processing tasks

### 3. Parallel - Multithreading
- Implemented using `concurrent.futures.ThreadPoolExecutor`
- Uses lightweight threads instead of full processes
- Shares memory between threads
- Lower overhead than multiprocessing
- Performance is affected by Python’s GIL


## Requirements
- Python 3.11
- OpenCV Library
- Numpy
- Matplotlib


## Results

### 1. Processed Images
Processed images are saved only for the **sequential implementation** to verify the correctness of the image processing pipeline.

The processed images are stored in the following directories:
- `results/100_images/` – processed output for the 100-image subset  
- `results/5000_images/` – processed output for the 5000-image subset  

Parallel implementations do not save output images in order to avoid saving duplicate processed images.


### 2. Performance Analysis
Performance is evaluated using the following metrics:
- Execution time  
- Speedup  
- Efficiency  

The sequential version is used as the baseline. Experiments are conducted using **100 and 5000 images** to analyse the impact of workload size on parallel performance.

The performance comparison is also **analysed using Amdahl’s Law** to evaluate theoretical speedup limits and understand scalability constraints caused by the sequential portion of the program.

Performance results are **visualised using graphs**, which are generated automatically and stored in the `results/graphs` directory.


## Google Cloud Platform (GCP) Configuration and Execution

### VM Configuration
All experiments were conducted on a Google Cloud Compute Engine virtual machine with the following configuration to ensure fair and consistent performance evaluation:

- Machine type: e2-standard-8  
- vCPUs: 8 (8 cores)  
- Memory: 32 GB  
- VM provisioning model: Standard  

### Execution Commands on GCP
### 1. Install Git 
    sudo apt update
    sudo apt install git -y
  
### 2. Clone Repository 
    git clone https://github.com/LeslieC-22/CST435-Parallel-Image-Processing.git
    cd CST435-Parallel-Image-Processing

### 3. Install Python venv support
    sudo apt install python3.11-venv -y
    
### 4. Create and Activate Virtual Environment
    python3.11 -m venv venv
    source venv/bin/activate

### 5. Install system OpenCV dependencies
    sudo apt install libgl1 libglib2.0-0 libsm6 libxext6 libxrender-dev -y
    
### 6. Install dependencies 
    pip install opencv-python numpy matplotlib

### 7. Run the programs
    python src/main.py



   
   
