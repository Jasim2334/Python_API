from rest_framework import serializers
from .models import *
from drf_extra_fields.fields import Base64ImageField


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('hno', 'street', 'city', 'state')


class WorkExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkExperience
        fields = ('companyName', 'fromDate', 'toDate', 'address')


class QualificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Qualification
        fields = ('qualificationName', 'fromDate', 'toDate', 'percentage')


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('title', 'description')


class PersonSerializer(serializers.ModelSerializer):
    photo = Base64ImageField()  # From DRF Extra Fields
    addressDetails = AddressSerializer(required=True)
    workExperience = WorkExperienceSerializer(many=True)
    qualifications = QualificationSerializer(many=True)
    projects = ProjectSerializer(many=True)

    def validate_email(self, value):
        email = value.lower()
        if Person.objects.filter(email=email).exists():
            raise serializers.ValidationError("employe already exist")
        return email

    class Meta:
        model = Person
        fields = ('name', 'email', 'age', 'gender', 'phoneNo',
                  'addressDetails', 'workExperience', 'qualifications', 'projects', 'photo')

    #THIS IS CREATE METHOD 
    def create(self, validated_data):
        address_data = validated_data.pop('addressDetails')
        work_experience_data = validated_data.pop('workExperience')
        qualifications_data = validated_data.pop('qualifications')
        projects_data = validated_data.pop('projects')

        address = AddressSerializer.create(
            AddressSerializer(), validated_data=address_data)
        work_experience = [WorkExperienceSerializer.create(WorkExperienceSerializer(
        ), validated_data=work_data) for work_data in work_experience_data]
        qualifications = [QualificationSerializer.create(QualificationSerializer(
        ), validated_data=qualification_data) for qualification_data in qualifications_data]
        projects = [ProjectSerializer.create(ProjectSerializer(
        ), validated_data=project_data) for project_data in projects_data]

        person = Person.objects.create(
            addressDetails=address, **validated_data)
        person.workExperience.set(work_experience)
        person.qualifications.set(qualifications)
        person.projects.set(projects)
        return person


    #THIS IS PUT AND PATCH METHOD
    def update(self, instance, validated_data):
        addressDetails_data = validated_data.get('addressDetails', {})
        if addressDetails_data:
            addressDetails = AddressSerializer(instance.addressDetails, data=addressDetails_data, partial=True)
            if addressDetails.is_valid():
                addressDetails.save()
        workExperience_data = validated_data.get('workExperience', [])
        for work_data in workExperience_data:
            work_experience = WorkExperienceSerializer(data=work_data, partial=True)
            if work_experience.is_valid():
                work_experience.save()
        qualifications_data = validated_data.get('qualifications',[])
        for qual_data in qualifications_data:
            qualification = QualificationSerializer(data=qual_data,partial=True)
            if qualification.is_valid():
                qualification.save()
        projects_data = validated_data.get('projects',[])
        for proj_data in projects_data:
            project = ProjectSerializer(data=proj_data,partial=True)
            if project.is_valid():
                project.save()
        instance.name = validated_data.get('name', instance.name)
        instance.email = validated_data.get('email', instance.email)
        instance.age = validated_data.get('age', instance.age)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.phoneNo = validated_data.get('phoneNo', instance.phoneNo)
        instance.photo = validated_data.get('photo', instance.photo)
        instance.save()

        address, created = Address.objects.update_or_create(person=instance,
                                                            defaults=addressDetails_data)
        for work in workExperience_data:
            workExperience, created = WorkExperience.objects.update_or_create(person=instance,
                                                                              defaults=work)
        for qualification in qualifications_data:
            qualification, created = Qualification.objects.update_or_create(person=instance,
                                                                            defaults=qualification)
        for project in projects_data:
            project, created = Project.objects.update_or_create(person=instance,
                                                                defaults=project)
        return instance

    #THIS IS DELETE METHOD
    def perform_destroy(self, instance):
        instance.delete()