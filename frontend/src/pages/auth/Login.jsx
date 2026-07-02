import { useForm } from "react-hook-form";
import { login } from "../../services/authService";

function Login() {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm();

const onSubmit = async (data) => {

    try {

        const response = await login(data);
                localStorage.setItem(
            "access_token",
            response.access_token
        );

        localStorage.setItem(
            "refresh_token",
            response.refresh_token
        );

        localStorage.setItem(
            "user",
            JSON.stringify(response.user)
        );

        console.log("Login Successful");

    }

    catch (error) {

        console.log(error);

    }

}

  return (
    <div className="container mt-5">
      <div className="row justify-content-center">
        <div className="col-md-4">
          <h2 className="mb-4">Login</h2>

          <form onSubmit={handleSubmit(onSubmit)}>
            {" "}
            <div className="mb-3">
              <label className="form-label">Email</label>

              <input
                type="email"
                className="form-control"
                {...register("email", {
                  required: "Email is required",
                })}
              />
              {errors.email && (
                <p className="text-danger">{errors.email.message}</p>
              )}
            </div>
            <div className="mb-3">
              <label className="form-label">Password</label>

              <input
                type="password"
                className="form-control"
                {...register("password", {
                  required: "Password is required",
                })}
              />

              {errors.password && (
                <p className="text-danger">{errors.password.message}</p>
              )}
            </div>
            <button className="btn btn-primary w-100">Login</button>
          </form>
        </div>
      </div>
    </div>
  );
}

export default Login;
