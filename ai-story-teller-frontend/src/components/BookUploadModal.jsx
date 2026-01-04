import React, { useState } from "react";
import { X, Upload, Loader2 } from "lucide-react";

function BookUploadModal({ isOpen, onClose, onUploadSuccess }) {
    const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;
    const [file, setFile] = useState(null);
    const [bookTitle, setBookTitle] = useState("");
    const [bookAuthor, setBookAuthor] = useState("");
    const [uploading, setUploading] = useState(false);
    const [error, setError] = useState("");

    const handleFileChange = (e) => {
        const selectedFile = e.target.files[0];
        if (selectedFile) {
            // Validate file type
            const validExtensions = [".pdf", ".txt", ".epub"];
            const fileExt = selectedFile.name.toLowerCase().match(/\.[^.]+$/)?.[0];

            if (!validExtensions.includes(fileExt)) {
                setError("Invalid file type. Please upload PDF, TXT, or EPUB files.");
                setFile(null);
                return;
            }

            // Validate file size (10MB limit)
            const maxSize = 10 * 1024 * 1024;
            if (selectedFile.size > maxSize) {
                setError("File size exceeds 10MB limit.");
                setFile(null);
                return;
            }

            setError("");
            setFile(selectedFile);

            // Auto-fill title from filename if not set
            if (!bookTitle) {
                const fileName = selectedFile.name.replace(/\.[^.]+$/, "");
                setBookTitle(fileName);
            }
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!file) {
            setError("Please select a file to upload");
            return;
        }

        setUploading(true);
        setError("");

        try {
            const formData = new FormData();
            formData.append("file", file);
            if (bookTitle) formData.append("book_title", bookTitle);
            if (bookAuthor) formData.append("book_author", bookAuthor);

            const response = await fetch(`${BACKEND_URL}/api/books/upload`, {
                method: "POST",
                body: formData,
                credentials: "include",
            });

            if (response.ok) {
                const data = await response.json();
                onUploadSuccess(data);
                handleClose();
            } else {
                const errorData = await response.json();
                setError(errorData.detail || "Failed to upload book");
            }
        } catch (error) {
            console.error("Error uploading book:", error);
            setError("An error occurred while uploading the book");
        } finally {
            setUploading(false);
        }
    };

    const handleClose = () => {
        setFile(null);
        setBookTitle("");
        setBookAuthor("");
        setError("");
        onClose();
    };

    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
            <div className="bg-white rounded-lg p-8 max-w-md w-full">
                <div className="flex justify-between items-center mb-6">
                    <h2 className="text-2xl font-bold">Upload Book</h2>
                    <button
                        onClick={handleClose}
                        className="text-gray-500 hover:text-gray-700"
                        disabled={uploading}
                    >
                        <X size={24} />
                    </button>
                </div>

                <form onSubmit={handleSubmit}>
                    {/* File Upload */}
                    <div className="mb-4">
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                            Book File (PDF, TXT, or EPUB)
                        </label>
                        <input
                            type="file"
                            accept=".pdf,.txt,.epub"
                            onChange={handleFileChange}
                            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                            disabled={uploading}
                            required
                        />
                        {file && (
                            <div className="mt-2 flex items-center text-sm text-gray-600">
                                <Upload size={16} className="mr-2" />
                                {file.name} ({(file.size / 1024).toFixed(1)} KB)
                            </div>
                        )}
                    </div>

                    {/* Book Title */}
                    <div className="mb-4">
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                            Book Title (Optional)
                        </label>
                        <input
                            type="text"
                            value={bookTitle}
                            onChange={(e) => setBookTitle(e.target.value)}
                            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                            placeholder="Enter book title"
                            disabled={uploading}
                        />
                    </div>

                    {/* Book Author */}
                    <div className="mb-4">
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                            Author (Optional)
                        </label>
                        <input
                            type="text"
                            value={bookAuthor}
                            onChange={(e) => setBookAuthor(e.target.value)}
                            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                            placeholder="Enter author name"
                            disabled={uploading}
                        />
                    </div>

                    {/* Error Message */}
                    {error && (
                        <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-md">
                            <p className="text-sm text-red-600">{error}</p>
                        </div>
                    )}

                    {/* Buttons */}
                    <div className="flex justify-end space-x-4">
                        <button
                            type="button"
                            onClick={handleClose}
                            className="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-gray-500"
                            disabled={uploading}
                        >
                            Cancel
                        </button>
                        <button
                            type="submit"
                            disabled={uploading || !file}
                            className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
                        >
                            {uploading ? (
                                <>
                                    <Loader2 className="animate-spin mr-2" size={16} />
                                    Uploading...
                                </>
                            ) : (
                                "Upload Book"
                            )}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
}

export default BookUploadModal;
