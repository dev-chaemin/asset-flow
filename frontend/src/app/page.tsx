export default async function Home() {
  const response = await fetch("http://127.0.0.1:8000/", {
    cache: "no-store",
  });

  const data = await response.json();

  return (
    <main className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="rounded-2xl bg-white p-10 shadow-sm">
        <h1 className="text-3xl font-bold">AssetFlow</h1>

        <p className="mt-4 text-gray-600">
          Backend response:
        </p>

        <p className="mt-2 font-semibold">
          {data.message}
        </p>
      </div>
    </main>
  );
}