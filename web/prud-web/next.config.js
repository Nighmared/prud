/** @type {import('next').NextConfig} */
const nextConfig = {
    async rewrites() {
        if (process.env.NODE_ENV === "development") {
            return [
                {
                    source: '/api/:path*',
                    destination: `http://localhost:8000/api/:path*`
                }
            ]
        }
    }
    ,

    output: 'standalone',
}

module.exports = nextConfig
