# GCS - Service Company Management System

A full-stack service company management system built with Next.js, React, TypeScript, and Prisma.

## Features

- Purchase management (vendors, POs, expenses, debit notes, payments)
- Sales management (customers, quotations, invoices, delivery challans, credit notes, payments, inquiries)
- PDF generation for invoices, quotations, and POs
- Excel import/export functionality
- Authentication with role-based access control

## Getting Started

### Prerequisites

- Node.js 16.x or later
- PostgreSQL database (or use Neon)

### Installation

1. Clone the repository
2. Install dependencies:

\`\`\`bash
npm install
\`\`\`

3. Copy the `.env.example` file to `.env` and update the environment variables:

\`\`\`bash
cp .env.example .env
\`\`\`

4. Set up your database connection in the `.env` file:

\`\`\`
DATABASE_URL="postgresql://username:password@localhost:5432/gcs_system"
\`\`\`

5. Run database migrations:

\`\`\`bash
npx prisma migrate dev
\`\`\`

6. Seed the database:

\`\`\`bash
npm run seed
\`\`\`

7. Start the development server:

\`\`\`bash
npm run dev
\`\`\`

### PDF Templates

To use the PDF generation feature, place your Excel templates in the `templates` directory:

- `templates/invoice-template.xlsx`
- `templates/quotation-template.xlsx`
- `templates/po-template.xlsx`

The system will use these templates to generate PDFs based on your data.

## Default Users

After running the seed script, you can log in with the following credentials:

- Admin: admin@example.com / admin123
- User: user@example.com / user123

## License

This project is licensed under the MIT License.
\`\`\`

This completes the core structure of the GCS service company management system. The system includes:

1. Prisma schema with all required models
2. Authentication system with role-based access control
3. API routes for CRUD operations
4. UI components for listing, viewing, creating, and editing records
5. PDF generation and Excel import/export functionality
6. Sample data seeding

To use the PDF generation feature, you'll need to place your Excel templates in the `templates` directory. The system will use these templates to generate PDFs based on your data.

You can extend this system by adding more features like:

1. Dashboard analytics and reporting
2. Email notifications
3. Advanced filtering and searching
4. Multi-currency support
5. Tax calculation rules
6. User management interface
