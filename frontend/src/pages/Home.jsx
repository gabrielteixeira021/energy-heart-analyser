import React from "react";
import Hero from "../components/homepage/Hero";
import Tools from "../components/homepage/Tools";
import Members from "../components/homepage/Members";
import Minimundos from "../components/homepage/Minimundos";
import Dashboards from "../components/homepage/Dashboards";

export default function Home() {
  return (
    <main className="main flex flex-col justify-center items-center w-full bg-gray-900">
      <Hero />
      <Members />
      <Tools />
      <Minimundos />
      <Dashboards />
    </main>
  );
}
