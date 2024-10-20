fetch('./data/data.yml')
.then(response => response.json()) // Parse the JSON file
.then(data => {
    // Function to access nested properties based on a key string
    function getNestedValue(obj, key) {
        return key.split('.').reduce((o, k) => (o || {})[k], obj);
    }

    // Loop through all elements with the 'user' attribute
    document.querySelectorAll('[user]').forEach(element => {
        // Get the variable name from the 'user' attribute (could be nested)
        const varName = element.getAttribute('user');
        // Get the nested value from the JSON using the helper function
        const value = getNestedValue(data, varName);

        // Check if the value exists in the JSON data
        if (value !== undefined) {
            // Set the content of the HTML element to the JSON value
            element.textContent = value;
        } else {
            element.textContent = `Variable ${varName} not found in JSON`;
        }
    });
})
.catch(error => console.error('Error fetching JSON:', error));