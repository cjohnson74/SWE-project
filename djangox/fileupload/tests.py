# fileupload/tests.py
from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import UploadedFile


class FileUploadTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.upload_url = reverse('fileupload:upload_file')
        self.success_url = reverse('fileupload:upload_success')

    def test_upload_file_success(self):
        # Create a small text file to upload
        test_file = SimpleUploadedFile(
            "testfile.txt", b"Test file content", content_type="text/plain"
        )

        # Send POST request with the file
        response = self.client.post(self.upload_url, {'file': test_file})

        # Check if the response redirects to the success page
        self.assertRedirects(response, self.success_url)

        # Check if the file is saved in the database
        self.assertEqual(UploadedFile.objects.count(), 1)
        uploaded_file = UploadedFile.objects.first()
        self.assertEqual(uploaded_file.file.name, 'uploads/testfile.txt')

    def test_upload_no_file(self):
        # Send POST request without a file
        response = self.client.post(self.upload_url, {})

        # Check if the form renders again with an error
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'file', 'This field is required.')

        # Check that no file is saved in the database
        self.assertEqual(UploadedFile.objects.count(), 0)

    def test_upload_invalid_file_type(self):
        # Create an invalid file type (e.g., an image with incorrect extension)
        test_file = SimpleUploadedFile(
            "testfile.exe", b"Fake executable content", content_type="application/octet-stream"
        )

        # Send POST request with the invalid file
        response = self.client.post(self.upload_url, {'file': test_file})

        # Check if the form renders again with an error (if validation added for file types)
        self.assertEqual(response.status_code, 200)

        # Check that no file is saved in the database
        self.assertEqual(UploadedFile.objects.count(), 0)