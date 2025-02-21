// src/app/signup/page.tsx
'use client'; // Mark this as a Client Component

export default function SignUpPage() {
  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    // Get form data
    const formData = new FormData(event.currentTarget);
    const firstName = formData.get('firstName')?.toString().toLowerCase() || '';
    const lastName = formData.get('lastName')?.toString().toLowerCase() || '';
    const email = formData.get('email')?.toString().toLowerCase() || '';
    const sport = formData.get('sport')?.toString().toLowerCase() || '';

    // Basic email validation
    if (!validateEmail(email)) {
      alert('Please enter a valid email address.');
      return;
    }

    // Prepare data for API call
    const userData = { firstName, lastName, email, sport };

    try {
      // Make API call to Flask backend
      const response = await fetch('/api/signup', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
      });

      if (response.ok) {
        alert('Sign up successful!');
        event.currentTarget.reset(); // Reset the form
      } else {
        alert('Sign up failed. Please try again.');
      }
    } catch (error) {
      console.error('Error:', error);
      alert('An error occurred. Please try again.');
    }
  };

  // Basic email validation function
  const validateEmail = (email: string) => {
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex.test(email);
  };

  return (
    <div className="bg-gray-100 flex items-center justify-center h-screen">
      <div className="bg-white p-8 rounded-lg shadow-lg w-96">
        <h1 className="text-2xl font-bold mb-6 text-center">Sign Up for Sports News</h1>
        <form onSubmit={handleSubmit} className="space-y-4">
          {/* First Name */}
          <div>
            <label htmlFor="firstName" className="block text-sm font-medium text-gray-700">First Name</label>
            <input type="text" id="firstName" name="firstName" required
                   className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500" />
          </div>
          {/* Last Name */}
          <div>
            <label htmlFor="lastName" className="block text-sm font-medium text-gray-700">Last Name</label>
            <input type="text" id="lastName" name="lastName" required
                   className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500" />
          </div>
          {/* Email */}
          <div>
            <label htmlFor="email" className="block text-sm font-medium text-gray-700">Email Address</label>
            <input type="email" id="email" name="email" required
                   className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500" />
          </div>
          {/* Sport Selection Dropdown */}
          <div>
            <label htmlFor="sport" className="block text-sm font-medium text-gray-700">Choose a Sport</label>
            <select id="sport" name="sport" required
                    className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500">
              <option value="" disabled selected>Select a sport</option>
              <option value="soccer">Soccer</option>
              <option value="football">Football</option>
              <option value="baseball">Baseball</option>
              <option value="cricket">Cricket</option>
              <option value="hockey">Hockey</option>
            </select>
          </div>
          {/* Submit Button */}
          <div>
            <button type="submit"
                    className="w-full bg-blue-500 text-white py-2 px-4 rounded-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2">
              Sign Up
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}