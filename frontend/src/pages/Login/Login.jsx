import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import Navbar from "../../components/common/Navbar";
import InputField from "../../components/forms/InputField";

function Login() {
  const [loginData, setLoginData] = useState({
    email: "",
    password: "",
  });
  const navigate = useNavigate();
  const handleChange = (e) => {
    setLoginData({
      ...loginData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = (e) => {
  e.preventDefault();

  console.log("Login Data:", loginData);

  navigate("/dashboard");
};

  return (
    <>
      <Navbar />

      <section className="min-h-screen bg-slate-50 flex items-center justify-center px-6 py-10">

        <div className="w-full max-w-5xl grid lg:grid-cols-2 shadow-2xl rounded-3xl overflow-hidden">

          {/* LEFT PANEL */}

          <div className="bg-[#1E3A8A] text-white p-12 flex flex-col justify-center">

            <h1 className="text-5xl font-bold">
              Welcome Back
            </h1>

            <p className="mt-6 text-blue-100 text-lg leading-8">
              Sign in to access your CitizenOne dashboard,
              upload documents, and discover government
              schemes recommended just for you.
            </p>

            <div className="mt-12 space-y-5">

              <div className="flex items-center gap-4">
                <span className="bg-white text-[#1E3A8A] rounded-full w-10 h-10 flex items-center justify-center font-bold">
                  ✓
                </span>

                <p>Personalized AI Recommendations</p>
              </div>

              <div className="flex items-center gap-4">
                <span className="bg-white text-[#1E3A8A] rounded-full w-10 h-10 flex items-center justify-center font-bold">
                  ✓
                </span>

                <p>Secure Document Storage</p>
              </div>

              <div className="flex items-center gap-4">
                <span className="bg-white text-[#1E3A8A] rounded-full w-10 h-10 flex items-center justify-center font-bold">
                  ✓
                </span>

                <p>Easy Scheme Applications</p>
              </div>

            </div>

          </div>

          {/* RIGHT PANEL */}

          <div className="bg-white p-10 lg:p-14">

            <h2 className="text-3xl font-bold text-gray-800">
              Login
            </h2>

            <p className="text-gray-500 mt-2">
              Sign in to continue.
            </p>

            <form
              onSubmit={handleSubmit}
              className="mt-10 space-y-6"
            >

              <InputField
                label="Email"
                type="email"
                name="email"
                value={loginData.email}
                onChange={handleChange}
                placeholder="example@email.com"
              />

              <InputField
                label="Password"
                type="password"
                name="password"
                value={loginData.password}
                onChange={handleChange}
                placeholder="Enter your password"
              />

              <button
                type="submit"
                className="w-full bg-[#1E3A8A] hover:bg-blue-800 text-white py-4 rounded-xl text-lg font-semibold transition"
              >
                Login
              </button>

            </form>

            <p className="text-center mt-8 text-gray-600">
              Don't have an account?{" "}
              <Link
                to="/register"
                className="text-[#1E3A8A] font-semibold hover:underline"
              >
                Register
              </Link>
            </p>

          </div>

        </div>

      </section>
    </>
  );
}

export default Login;