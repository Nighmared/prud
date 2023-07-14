/** @type {import('next').NextConfig} */
const nextConfig = {
    async rewrites() {
        return [
            {
                source: '/api/:path*',
                destination: `http://${process.env.WEB_API_HOST}:${process.env.WEB_API_PORT}/api/:path*`
            }
        ]
    },
    output: 'standalone',
}

module.exports = nextConfig
