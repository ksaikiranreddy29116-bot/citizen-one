
import { useState } from "react";
import { useNavigate } from "react-router-dom";

import Navbar from "../../components/common/Navbar";
import InputField from "../../components/forms/InputField";
import SelectField from "../../components/forms/SelectField";

import {
  genderOptions,
  educationOptions,
  casteOptions,
} from "../../constants/formOptions";

function Register() {
  const [formData, setFormData] = useState({
  fullName: "",
  age: "",
  gender: "",
  phone: "",
  email: "",
  educationLevel: "",
  occupation: "",
  state: "",
  district: "",
  annualIncome: "",
  casteCategory: "",
});
const navigate = useNavigate();
const handleChange = (e) => {

   setFormData({

      ...formData,

      [e.target.name]: e.target.value,

   });

};
const handleSubmit = (e) => {
  e.preventDefault();

  console.log("Submitted Data:", formData);

  navigate("/login");
};
console.log(formData);
  return (
    <>
      <Navbar />

      <section className="min-h-screen bg-slate-50 flex items-center justify-center px-6 py-10">

        <div className="w-full max-w-7xl grid lg:grid-cols-2 shadow-2xl rounded-3xl overflow-hidden">

          {/* LEFT PANEL */}

          <div className="bg-[#1E3A8A] text-white p-12 flex flex-col justify-center">

            <h1 className="text-5xl font-bold leading-tight">
              Join CitizenOne
            </h1>

            <p className="mt-6 text-lg text-blue-100 leading-8">
              Create your profile once and let CitizenOne
              discover the government schemes you are eligible for.
            </p>

            <div className="mt-12 space-y-8">

              <div className="flex items-start gap-4">

                <div className="bg-white text-[#1E3A8A] rounded-full w-10 h-10 flex items-center justify-center font-bold">
                  1
                </div>

                <div>

                  <h3 className="font-semibold text-xl">
                    Create your profile
                  </h3>

                  <p className="text-blue-100 mt-1">
                    Tell us about yourself once.
                  </p>

                </div>

              </div>

              <div className="flex items-start gap-4">

                <div className="bg-white text-[#1E3A8A] rounded-full w-10 h-10 flex items-center justify-center font-bold">
                  2
                </div>

                <div>

                  <h3 className="font-semibold text-xl">
                    Upload Documents
                  </h3>

                  <p className="text-blue-100 mt-1">
                    Verify documents securely.
                  </p>

                </div>

              </div>

              <div className="flex items-start gap-4">

                <div className="bg-white text-[#1E3A8A] rounded-full w-10 h-10 flex items-center justify-center font-bold">
                  3
                </div>

                <div>

                  <h3 className="font-semibold text-xl">
                    Get AI Recommendations
                  </h3>

                  <p className="text-blue-100 mt-1">
                    Instantly discover matching welfare schemes.
                  </p>

                </div>

              </div>

            </div>

          </div>

          {/* RIGHT PANEL */}

          <div className="bg-white p-10 lg:p-14">

            <h2 className="text-3xl font-bold text-gray-800">
              Create Account
            </h2>

            <p className="text-gray-500 mt-2">
              Complete your information to get started.
            </p>

            <form onSubmit={handleSubmit} className="mt-10 space-y-8">

  {/* PERSONAL INFORMATION */}

  <div>

    <h3 className="text-lg font-semibold text-gray-800 mb-4">
      Personal Information
    </h3>

    <div className="grid grid-cols-2 gap-5">

      <InputField
    label="Full Name"
    type="text"
    name="fullName"
    value={formData.fullName}
    onChange={handleChange}
    placeholder="Rahul Kumar"
  />

      <InputField
    label="Age"
    type="number"
    name="age"
    value={formData.age}
    onChange={handleChange}
    placeholder="20"
  />

       <SelectField
    label="Gender"
    name="gender"
    value={formData.gender}
    onChange={handleChange}
    options={genderOptions}
  />

      <InputField
    label="Phone"
    type="text"
    name="phone"
    value={formData.phone}
    onChange={handleChange}
    placeholder="9876543210"
  />

      <div className="col-span-2">
    <InputField
      label="Email"
      type="email"
      name="email"
      value={formData.email}
      onChange={handleChange}
      placeholder="example@email.com"
    />
  </div>

    </div>

  </div>

  {/* EDUCATION */}

  <div>

    <h3 className="text-lg font-semibold text-gray-800 mb-4">
      Education & Occupation
    </h3>

    <div className="grid grid-cols-2 gap-5">

       <SelectField
    label="Education Level"
    name="educationLevel"
    value={formData.educationLevel}
    onChange={handleChange}
    options={educationOptions}
  />

     <InputField
    label="Occupation"
    type="text"
    name="occupation"
    value={formData.occupation}
    onChange={handleChange}
    placeholder="Student"
  />

    </div>

  </div>

  {/* LOCATION */}

  <div>

    <h3 className="text-lg font-semibold text-gray-800 mb-4">
      Location
    </h3>

    <div className="grid grid-cols-2 gap-5">

      <InputField
    label="State"
    type="text"
    name="state"
    value={formData.state}
    onChange={handleChange}
    placeholder="Andhra Pradesh"
  />

      <InputField
    label="District"
    type="text"
    name="district"
    value={formData.district}
    onChange={handleChange}
    placeholder="Guntur"
  />

    </div>

  </div>

  {/* ELIGIBILITY */}

  <div>

    <h3 className="text-lg font-semibold text-gray-800 mb-4">
      Eligibility Details
    </h3>

    <div className="grid grid-cols-2 gap-5">

      <InputField
    label="Annual Income"
    type="number"
    name="annualIncome"
    value={formData.annualIncome}
    onChange={handleChange}
    placeholder="120000"
  />

     <SelectField
    label="Caste Category"
    name="casteCategory"
    value={formData.casteCategory}
    onChange={handleChange}
    options={casteOptions}
  />

    </div>

  </div>

  <button
  type="submit"
  className="w-full bg-[#1E3A8A] hover:bg-blue-800 text-white py-4 rounded-xl text-lg font-semibold transition"
>
  Create Citizen Profile
</button>

</form>

          </div>

        </div>

      </section>
    </>
  );
}

export default Register;