import { useState } from 'react';
import { Upload, Link2 } from 'lucide-react';

export default function AdInput({ onInputChange, isLoading }) {
  const [activeTab, setActiveTab] = useState('upload');
  const [previewImage, setPreviewImage] = useState(null);

  const handleFileUpload = (e) => {
    const file = e.target.files?.[0];
    if (file) {
      if (file.size > 5 * 1024 * 1024) {
        alert('Image must be under 5MB');
        return;
      }
      setPreviewImage(URL.createObjectURL(file));
      onInputChange(file, 'file');
    }
  };

  const handleUrlInput = (e) => {
    const url = e.target.value;
    if (url) {
      onInputChange(url, 'url');
    }
  };

  return (
    <div className="troopod-card p-6">
      <h3 className="font-syne text-lg font-bold mb-4">Ad Creative</h3>
      
      <div className="flex gap-2 mb-4 border-b border-border">
        <button
          onClick={() => setActiveTab('upload')}
          className={`px-4 py-2 font-dm-sans transition-colors ${
            activeTab === 'upload'
              ? 'border-b-2 border-accent-purple text-accent-purple'
              : 'text-text-secondary hover:text-text-primary'
          }`}
        >
          <Upload className="inline mr-2 w-4 h-4" />
          Upload Image
        </button>
        <button
          onClick={() => setActiveTab('url')}
          className={`px-4 py-2 font-dm-sans transition-colors ${
            activeTab === 'url'
              ? 'border-b-2 border-accent-purple text-accent-purple'
              : 'text-text-secondary hover:text-text-primary'
          }`}
        >
          <Link2 className="inline mr-2 w-4 h-4" />
          From URL
        </button>
      </div>

      {activeTab === 'upload' && (
        <div className="space-y-4">
          <div className="border-2 border-dashed border-border rounded-lg p-8 text-center hover:border-border-hover transition-colors cursor-pointer">
            <input
              type="file"
              accept="image/*"
              onChange={handleFileUpload}
              disabled={isLoading}
              className="hidden"
              id="file-upload"
            />
            <label htmlFor="file-upload" className="cursor-pointer">
              <Upload className="w-8 h-8 mx-auto mb-2 text-accent-purple" />
              <p className="text-text-secondary">Drag and drop or click to upload</p>
              <p className="text-text-muted text-sm">Max 5MB • PNG, JPG, GIF</p>
            </label>
          </div>
          {previewImage && (
            <img src={previewImage} alt="Preview" className="w-full rounded-lg h-40 object-cover" />
          )}
        </div>
      )}

      {activeTab === 'url' && (
        <div>
          <input
            type="url"
            onChange={handleUrlInput}
            disabled={isLoading}
            placeholder="https://your-ad-link.com"
            className="w-full bg-bg-secondary border border-border rounded-lg px-4 py-3 text-text-primary placeholder-text-muted focus:outline-none focus:border-accent-purple transition-colors"
          />
          <p className="text-text-muted text-sm mt-2">We'll screenshot your ad automatically</p>
        </div>
      )}
    </div>
  );
}
