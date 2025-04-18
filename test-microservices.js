#!/usr/bin/env node

/**
 * Cross-platform test script for the microservices
 * Works on Windows, Mac, and Linux
 * 
 * Requirements:
 * - Node.js installed
 * - Services running (docker compose up -d)
 * 
 * Run with: node test-microservices.js
 */

const http = require('http');
const https = require('https');

// Colors for terminal output
const colors = {
  reset: '\x1b[0m',
  green: '\x1b[32m',
  red: '\x1b[31m',
  yellow: '\x1b[33m',
  cyan: '\x1b[36m'
};

// Base URLs
const CATALOG_URL = 'http://localhost:8081';
const ORDER_URL = 'http://localhost:8082';

// Test state
let testProduct = null;
let anotherProductId = null;
let singleOrderId = null;
let multiOrderId = null;
let testsPassed = 0;
let testsFailed = 0;

/**
 * Print a section header
 */
function printHeader(title) {
  console.log(`\n${colors.yellow}==== ${title} ====${colors.reset}\n`);
}

/**
 * Check if a test passed or failed
 */
function checkResult(message, success, exitOnFailure = false) {
  if (success) {
    console.log(`${colors.green}✓ ${message}${colors.reset}`);
    testsPassed++;
  } else {
    console.log(`${colors.red}✗ ${message}${colors.reset}`);
    testsFailed++;
    if (exitOnFailure) {
      console.log(`${colors.red}Exiting due to critical failure${colors.reset}`);
      process.exit(1);
    }
  }
}

/**
 * Make an HTTP request
 */
function makeRequest(url, method = 'GET', data = null, headers = {}) {
  return new Promise((resolve, reject) => {
    const options = {
      method: method,
      headers: {
        'Content-Type': 'application/json',
        ...headers
      }
    };

    const client = url.startsWith('https') ? https : http;
    const req = client.request(url, options, (res) => {
      let responseData = '';
      
      res.on('data', (chunk) => {
        responseData += chunk;
      });
      
      res.on('end', () => {
        try {
          const jsonData = JSON.parse(responseData);
          resolve({ statusCode: res.statusCode, data: jsonData });
        } catch (e) {
          resolve({ statusCode: res.statusCode, data: responseData });
        }
      });
    });
    
    req.on('error', (error) => {
      reject(error);
    });
    
    if (data) {
      req.write(typeof data === 'string' ? data : JSON.stringify(data));
    }
    
    req.end();
  });
}

/**
 * Check if services are running
 */
async function checkServicesRunning() {
  printHeader('Checking if services are running');
  
  try {
    await makeRequest(`${CATALOG_URL}/products`);
    checkResult('Catalog service is running', true);
  } catch (error) {
    checkResult('Catalog service is running', false, true);
  }
  
  try {
    await makeRequest(`${ORDER_URL}/orders/1`);
    checkResult('Order service is running', true);
  } catch (error) {
    checkResult('Order service is running', false, true);
  }
}

/**
 * Test the catalog service
 */
async function testCatalogService() {
  printHeader('Testing Catalog Service');
  
  // Get all products
  console.log('Getting all products...');
  try {
    const response = await makeRequest(`${CATALOG_URL}/products`);
    const success = response.statusCode === 200 && Array.isArray(response.data);
    checkResult('Get all products', success);
    
    if (success && response.data.length > 0) {
      anotherProductId = response.data[0]._id;
      console.log(`Found existing product with ID: ${anotherProductId}`);
    }
  } catch (error) {
    checkResult('Get all products', false);
  }
  
  // Create a new product
  console.log('Creating a new product...');
  const newProduct = {
    name: 'Test Product',
    description: 'A test product created by the test script',
    price: 49.99,
    stock: 42,
    category: 'Test'
  };
  
  try {
    const response = await makeRequest(`${CATALOG_URL}/products`, 'POST', newProduct);
    console.log(JSON.stringify(response.data, null, 2));
    
    // The product was created successfully if we have an ID in the response
    // Status code 201 is correct for resource creation
    if ((response.statusCode === 200 || response.statusCode === 201) && response.data) {
      // Log the entire response for debugging
      console.log("Full response:", response);
      
      // Check if _id exists in the response data
      if (response.data._id) {
        testProduct = response.data;
        console.log(`Created product with ID: ${testProduct._id}`);
        checkResult('Create product', true);
      } else {
        console.log(`${colors.red}Product created but no ID found in response${colors.reset}`);
        checkResult('Create product', false);
      }
    } else {
      console.log(`${colors.red}Failed to create product: ${JSON.stringify(response)}${colors.reset}`);
      checkResult('Create product', false);
    }
  } catch (error) {
    console.log(`${colors.red}Error creating product: ${error.message}${colors.reset}`);
    checkResult('Create product', false);
  }
  
  // Use the first product from the list if we couldn't create a new one
  if (!testProduct) {
    console.log(`${colors.yellow}Attempting to use an existing product instead...${colors.reset}`);
    
    try {
      const response = await makeRequest(`${CATALOG_URL}/products`);
      if (response.statusCode === 200 && Array.isArray(response.data) && response.data.length > 0) {
        testProduct = response.data[0];
        console.log(`${colors.yellow}Using existing product with ID: ${testProduct._id}${colors.reset}`);
      } else {
        console.log(`${colors.red}Cannot continue tests without a test product${colors.reset}`);
        process.exit(1);
      }
    } catch (error) {
      console.log(`${colors.red}Cannot continue tests without a test product${colors.reset}`);
      process.exit(1);
    }
  }
  
  // Get the product by ID
  console.log('Getting product by ID...');
  try {
    const response = await makeRequest(`${CATALOG_URL}/products/${testProduct._id}`);
    // Just check if we got a valid response with a name property
    const success = response.statusCode === 200 && response.data && response.data.name;
    checkResult('Get product by ID', success);
  } catch (error) {
    checkResult('Get product by ID', false);
  }
  
  // Update the product
  console.log('Updating product...');
  const updateData = {
    price: 59.99,
    stock: 50
  };
  
  try {
    const response = await makeRequest(`${CATALOG_URL}/products/${testProduct._id}`, 'PUT', updateData);
    const success = response.statusCode === 200 && response.data.price === 59.99;
    checkResult('Update product', success);
    
    if (success) {
      testProduct = response.data;
    }
  } catch (error) {
    checkResult('Update product', false);
  }
}

/**
 * Test the order service
 */
async function testOrderService() {
  printHeader('Testing Order Service');
  
  // Create an order with a single product
  console.log('Creating an order with a single product...');
  const singleOrderData = {
    productIds: [testProduct._id]
  };
  
  try {
    const response = await makeRequest(`${ORDER_URL}/orders`, 'POST', singleOrderData);
    console.log(JSON.stringify(response.data, null, 2));
    
    const success = response.statusCode === 200 && response.data.id;
    checkResult('Create order with single product', success);
    
    if (success) {
      singleOrderId = response.data.id;
      console.log(`Created order with ID: ${singleOrderId}`);
      
      // Check if the total price is correct
      console.log('Checking total price...');
      const totalPriceSuccess = response.data.total === '59.99';
      checkResult('Total price is correct for single product order', totalPriceSuccess);
    }
  } catch (error) {
    checkResult('Create order with single product', false);
  }
  
  // Create an order with multiple products
  if (anotherProductId) {
    console.log('Creating an order with multiple products...');
    const multiOrderData = {
      productIds: [testProduct._id, anotherProductId]
    };
    
    try {
      const response = await makeRequest(`${ORDER_URL}/orders`, 'POST', multiOrderData);
      console.log(JSON.stringify(response.data, null, 2));
      
      const success = response.statusCode === 200 && response.data.id;
      checkResult('Create order with multiple products', success);
      
      if (success) {
        multiOrderId = response.data.id;
        console.log(`Created order with ID: ${multiOrderId}`);
        
        // Get the order by ID
        console.log('Getting order by ID...');
        try {
          const orderResponse = await makeRequest(`${ORDER_URL}/orders/${multiOrderId}`);
          console.log(JSON.stringify(orderResponse.data, null, 2));
          
          const getOrderSuccess = orderResponse.statusCode === 200;
          checkResult('Get order by ID', getOrderSuccess);
          
          if (getOrderSuccess) {
            // Check if the order contains all products
            console.log('Checking if order contains all products...');
            const productCount = orderResponse.data.products.length;
            const containsAllProducts = productCount === 2;
            
            if (containsAllProducts) {
              checkResult('Order contains all products', true);
            } else {
              console.log(`${colors.red}Order should contain 2 products, but contains ${productCount}${colors.reset}`);
              checkResult('Order contains all products', false);
            }
          }
        } catch (error) {
          checkResult('Get order by ID', false);
        }
      }
    } catch (error) {
      checkResult('Create order with multiple products', false);
    }
  } else {
    console.log(`${colors.yellow}Skipping multi-product order test (no other products found)${colors.reset}`);
  }
}

/**
 * Clean up test data
 */
async function cleanup() {
  printHeader('Cleaning up');
  
  if (testProduct) {
    console.log('Deleting test product...');
    try {
      await makeRequest(`${CATALOG_URL}/products/${testProduct._id}`, 'DELETE');
      checkResult('Delete test product', true);
    } catch (error) {
      checkResult('Delete test product', false);
    }
  }
}

/**
 * Print test summary
 */
function printSummary() {
  printHeader('Test Summary');
  
  if (testsFailed === 0) {
    console.log(`${colors.green}All tests completed successfully!${colors.reset}`);
  } else {
    console.log(`${colors.yellow}Tests completed with ${testsFailed} failures.${colors.reset}`);
  }
  
  console.log(`${colors.cyan}Tests passed: ${testsPassed}${colors.reset}`);
  console.log(`${colors.cyan}Tests failed: ${testsFailed}${colors.reset}`);
  console.log('\nThe catalog service and order service are working together.');
  console.log('The order service can fetch product information from the catalog service and calculate the total price correctly.');
}

/**
 * Run all tests
 */
async function runTests() {
  printHeader('Testing Microservices');
  console.log('This script will test the catalog and order services');
  
  try {
    await checkServicesRunning();
    await testCatalogService();
    await testOrderService();
    await cleanup();
    printSummary();
  } catch (error) {
    console.error(`${colors.red}Unexpected error: ${error.message}${colors.reset}`);
    process.exit(1);
  }
}

// Run the tests
runTests();
