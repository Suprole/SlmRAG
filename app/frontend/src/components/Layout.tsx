import React from "react";
import { Link } from "react-router-dom";

type LayoutProps = {
  children: React.ReactNode;
};

const Layout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <div className="min-h-screen flex flex-col">
      <header className="bg-white shadow-sm border-b border-secondary-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <Link to="/" className="flex items-center space-x-2">
              <svg
                className="w-8 h-8 text-primary-600"
                fill="currentColor"
                viewBox="0 0 24 24"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path d="M19.219 9.219c-1.499 0-3.021.253-4.219.707V5c0-1.103-.897-2-2-2H5c-1.103 0-2 .897-2 2v14c0 1.103.897 2 2 2h8c1.103 0 2-.897 2-2v-1.219c1.968.573 3.766.808 4.219.808C20.756 18.589 22 17.35 22 14.999v-1.781c0-2.351-1.244-3.999-2.781-3.999zM13 19H5V5h8v14zm7-4.001c0 1.095-.539 1.843-1.016 1.936-.603-.118-2.252-.404-3.984-.967V12.03c1.732-.562 3.381-.848 3.984-.966.478.092 1.016.841 1.016 1.935v1.998z" />
              </svg>
              <span className="text-xl font-semibold text-primary-600">RAG Chat</span>
            </Link>
            <div className="flex items-center space-x-4">
              <Link to="/" className="text-secondary-600 hover:text-primary-600 transition-colors">
                ホーム
              </Link>
              <a
                href="https://github.com/yourusername/ragchat"
                target="_blank"
                rel="noopener noreferrer"
                className="text-secondary-600 hover:text-primary-600 transition-colors"
              >
                GitHub
              </a>
            </div>
          </div>
        </div>
      </header>
      <main className="flex-grow">{children}</main>
      <footer className="bg-white border-t border-secondary-200 py-4">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <p className="text-center text-secondary-500 text-sm">
            &copy; {new Date().getFullYear()} RAG Chat | PDFを読み込み、対話しよう
          </p>
        </div>
      </footer>
    </div>
  );
};

export default Layout; 