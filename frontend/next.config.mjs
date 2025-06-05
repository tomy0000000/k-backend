/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: "https",
        hostname: "img.tomy.me",
        port: "",
      },
    ],
  },
};

export default nextConfig;
