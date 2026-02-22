export default function ProcessBackground({ currentStep = 1 }) {
  const steps = [
    "Uploaded",
    "Extracting",
    "Waiting for Driver Confirmation",
    "Evaluating",
    "Final Output",
  ];

  return (
    <div className="relative min-h-screen flex items-center justify-center">
      {/* Background */}
      <div
        className="absolute inset-0 bg-cover bg-center"
        style={{
          backgroundImage:
            "url('https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?q=80&w=2070&auto=format&fit=crop')",
        }}
      />
      <div className="absolute inset-0 bg-black/70 backdrop-blur-sm" />

      <div className="relative z-10 w-full max-w-6xl px-6 py-12">
        <h1 className="text-3xl md:text-5xl font-bold text-white mb-12 tracking-wide text-center md:text-left">
          BORDERPILOT AI
        </h1>

        {/* DESKTOP VIEW */}
        <div className="hidden md:flex items-center justify-between">
          {steps.map((step, index) => {
            const stepNumber = index + 1;
            const isActive = stepNumber === currentStep;
            const isCompleted = stepNumber < currentStep;

            return (
              <div
                key={step}
                className="flex-1 flex flex-col items-center relative"
              >
                {index !== steps.length - 1 && (
                  <div
                    className={`absolute top-5 left-1/2 w-full h-1 ${
                      isCompleted ? "bg-green-500" : "bg-gray-600"
                    }`}
                  />
                )}

                <div
                  className={`w-10 h-10 rounded-full flex items-center justify-center text-sm font-bold z-10
                    ${
                      isCompleted
                        ? "bg-green-500 text-black"
                        : isActive
                          ? "bg-blue-500 text-white"
                          : "bg-gray-600 text-gray-300"
                    }`}
                >
                  {stepNumber}
                </div>

                <p className="mt-4 text-sm text-gray-300 text-center max-w-[140px]">
                  {step}
                </p>
              </div>
            );
          })}
        </div>

        {/* MOBILE VIEW */}
        <div className="md:hidden space-y-8">
          {steps.map((step, index) => {
            const stepNumber = index + 1;
            const isActive = stepNumber === currentStep;
            const isCompleted = stepNumber < currentStep;

            return (
              <div key={step} className="flex items-center gap-4">
                <div
                  className={`w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold
                    ${
                      isCompleted
                        ? "bg-green-500 text-black"
                        : isActive
                          ? "bg-blue-500 text-white"
                          : "bg-gray-600 text-gray-300"
                    }`}
                >
                  {stepNumber}
                </div>

                <p className="text-sm text-gray-300">{step}</p>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
