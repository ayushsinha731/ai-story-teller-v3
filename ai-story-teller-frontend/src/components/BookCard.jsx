import React from "react";
import { Trash2, Book } from "lucide-react";

function BookCard({ book, onDelete }) {
    const formatFileSize = (bytes) => {
        if (bytes < 1024) return `${bytes} B`;
        if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
        return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
    };

    const handleDelete = () => {
        if (window.confirm(`Are you sure you want to delete "${book.bookTitle}"?`)) {
            onDelete(book.id);
        }
    };

    return (
        <div className="bg-white rounded-lg shadow-md p-4 hover:shadow-lg transition-shadow">
            <div className="flex items-start justify-between">
                <div className="flex items-start space-x-3 flex-1">
                    <div className="bg-blue-100 p-3 rounded-lg">
                        <Book className="text-blue-600" size={24} />
                    </div>
                    <div className="flex-1 min-w-0">
                        <h3 className="font-semibold text-gray-800 truncate">
                            {book.bookTitle}
                        </h3>
                        {book.bookAuthor && (
                            <p className="text-sm text-gray-600 truncate">
                                by {book.bookAuthor}
                            </p>
                        )}
                        <div className="flex items-center space-x-2 mt-2">
                            <span className="text-xs bg-gray-100 px-2 py-1 rounded">
                                {book.fileType.toUpperCase()}
                            </span>
                            <span className="text-xs text-gray-500">
                                {formatFileSize(book.fileSize)}
                            </span>
                        </div>
                        <p className="text-xs text-gray-400 mt-1">
                            Uploaded {new Date(book.uploadDate).toLocaleDateString()}
                        </p>
                    </div>
                </div>
                <button
                    onClick={handleDelete}
                    className="text-red-500 hover:text-red-700 p-2 hover:bg-red-50 rounded"
                    title="Delete book"
                >
                    <Trash2 size={18} />
                </button>
            </div>
        </div>
    );
}

export default BookCard;
