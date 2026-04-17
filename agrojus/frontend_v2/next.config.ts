import type { NextConfig } from "next";
import path from "node:path";

const nextConfig: NextConfig = {
  turbopack: {
    // Caminho absoluto elimina o warning "turbopack.root should be absolute"
    root: path.resolve(__dirname),
  },
};

export default nextConfig;
