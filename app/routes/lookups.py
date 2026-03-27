from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from app.auth import get_current_user
from app.lookups_api import service
from app.lookups_api.schemas import (
    CampusCreate,
    CampusResponse,
    CampusUpdate,
    CollegeCreate,
    CollegeResponse,
    CollegeUpdate,
    DepartmentCreate,
    DepartmentResponse,
    DepartmentUpdate,
    SchoolYearCreate,
    SchoolYearResponse,
    SchoolYearUpdate,
    SemesterCreate,
    SemesterResponse,
    SemesterUpdate,
)
from database.database import get_db


router = APIRouter(prefix="/lookups", tags=["Lookups"])


@router.post("/campuses", response_model=CampusResponse, status_code=status.HTTP_201_CREATED)
def create_campus(payload: CampusCreate, db=Depends(get_db), _: dict = Depends(get_current_user)):
    return service.create_campus(db, payload)


@router.get("/campuses", response_model=list[CampusResponse])
def list_campuses(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db=Depends(get_db),
<<<<<<< HEAD
=======
    _: dict = Depends(get_current_user),
>>>>>>> b96a08110657e89c15f427110eb642caa7c9a340
):
    return service.list_campuses(db, skip, limit)


@router.get("/campuses/{campus_id}", response_model=CampusResponse)
<<<<<<< HEAD
def get_campus(campus_id: UUID, db=Depends(get_db)):
=======
def get_campus(campus_id: UUID, db=Depends(get_db), _: dict = Depends(get_current_user)):
>>>>>>> b96a08110657e89c15f427110eb642caa7c9a340
    return service.get_campus(db, str(campus_id))


@router.put("/campuses/{campus_id}", response_model=CampusResponse)
def update_campus(campus_id: UUID, payload: CampusUpdate, db=Depends(get_db), _: dict = Depends(get_current_user)):
    return service.update_campus(db, str(campus_id), payload)


@router.delete("/campuses/{campus_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_campus(campus_id: UUID, db=Depends(get_db), _: dict = Depends(get_current_user)):
    service.delete_campus(db, str(campus_id))
    return None


@router.post("/colleges", response_model=CollegeResponse, status_code=status.HTTP_201_CREATED)
def create_college(payload: CollegeCreate, db=Depends(get_db), _: dict = Depends(get_current_user)):
    return service.create_college(db, payload)


@router.get("/colleges", response_model=list[CollegeResponse])
def list_colleges(
    campus_id: UUID | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db=Depends(get_db),
<<<<<<< HEAD
=======
    _: dict = Depends(get_current_user),
>>>>>>> b96a08110657e89c15f427110eb642caa7c9a340
):
    return service.list_colleges(db, str(campus_id) if campus_id else None, skip, limit)


@router.get("/colleges/{college_id}", response_model=CollegeResponse)
<<<<<<< HEAD
def get_college(college_id: UUID, db=Depends(get_db)):
=======
def get_college(college_id: UUID, db=Depends(get_db), _: dict = Depends(get_current_user)):
>>>>>>> b96a08110657e89c15f427110eb642caa7c9a340
    return service.get_college(db, str(college_id))


@router.put("/colleges/{college_id}", response_model=CollegeResponse)
def update_college(college_id: UUID, payload: CollegeUpdate, db=Depends(get_db), _: dict = Depends(get_current_user)):
    return service.update_college(db, str(college_id), payload)


@router.delete("/colleges/{college_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_college(college_id: UUID, db=Depends(get_db), _: dict = Depends(get_current_user)):
    service.delete_college(db, str(college_id))
    return None


@router.post("/departments", response_model=DepartmentResponse, status_code=status.HTTP_201_CREATED)
def create_department(payload: DepartmentCreate, db=Depends(get_db), _: dict = Depends(get_current_user)):
    return service.create_department(db, payload)


@router.get("/departments", response_model=list[DepartmentResponse])
def list_departments(
    college_id: UUID | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db=Depends(get_db),
<<<<<<< HEAD
=======
    _: dict = Depends(get_current_user),
>>>>>>> b96a08110657e89c15f427110eb642caa7c9a340
):
    return service.list_departments(db, str(college_id) if college_id else None, skip, limit)


@router.get("/departments/{department_id}", response_model=DepartmentResponse)
<<<<<<< HEAD
def get_department(department_id: UUID, db=Depends(get_db)):
=======
def get_department(department_id: UUID, db=Depends(get_db), _: dict = Depends(get_current_user)):
>>>>>>> b96a08110657e89c15f427110eb642caa7c9a340
    return service.get_department(db, str(department_id))


@router.put("/departments/{department_id}", response_model=DepartmentResponse)
def update_department(
    department_id: UUID,
    payload: DepartmentUpdate,
    db=Depends(get_db),
    _: dict = Depends(get_current_user),
):
    return service.update_department(db, str(department_id), payload)


@router.delete("/departments/{department_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_department(department_id: UUID, db=Depends(get_db), _: dict = Depends(get_current_user)):
    service.delete_department(db, str(department_id))
    return None


@router.post("/school-years", response_model=SchoolYearResponse, status_code=status.HTTP_201_CREATED)
def create_school_year(payload: SchoolYearCreate, db=Depends(get_db), _: dict = Depends(get_current_user)):
    return service.create_school_year(db, payload)


@router.get("/school-years", response_model=list[SchoolYearResponse])
def list_school_years(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db=Depends(get_db),
<<<<<<< HEAD
=======
    _: dict = Depends(get_current_user),
>>>>>>> b96a08110657e89c15f427110eb642caa7c9a340
):
    return service.list_school_years(db, skip, limit)


@router.get("/school-years/{school_year_id}", response_model=SchoolYearResponse)
<<<<<<< HEAD
def get_school_year(school_year_id: UUID, db=Depends(get_db)):
=======
def get_school_year(school_year_id: UUID, db=Depends(get_db), _: dict = Depends(get_current_user)):
>>>>>>> b96a08110657e89c15f427110eb642caa7c9a340
    return service.get_school_year(db, str(school_year_id))


@router.put("/school-years/{school_year_id}", response_model=SchoolYearResponse)
def update_school_year(
    school_year_id: UUID,
    payload: SchoolYearUpdate,
    db=Depends(get_db),
    _: dict = Depends(get_current_user),
):
    return service.update_school_year(db, str(school_year_id), payload)


@router.delete("/school-years/{school_year_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_school_year(school_year_id: UUID, db=Depends(get_db), _: dict = Depends(get_current_user)):
    service.delete_school_year(db, str(school_year_id))
    return None


@router.post("/semesters", response_model=SemesterResponse, status_code=status.HTTP_201_CREATED)
def create_semester(payload: SemesterCreate, db=Depends(get_db), _: dict = Depends(get_current_user)):
    return service.create_semester(db, payload)


@router.get("/semesters", response_model=list[SemesterResponse])
def list_semesters(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db=Depends(get_db),
<<<<<<< HEAD
=======
    _: dict = Depends(get_current_user),
>>>>>>> b96a08110657e89c15f427110eb642caa7c9a340
):
    return service.list_semesters(db, skip, limit)


@router.get("/semesters/{semester_id}", response_model=SemesterResponse)
<<<<<<< HEAD
def get_semester(semester_id: UUID, db=Depends(get_db)):
=======
def get_semester(semester_id: UUID, db=Depends(get_db), _: dict = Depends(get_current_user)):
>>>>>>> b96a08110657e89c15f427110eb642caa7c9a340
    return service.get_semester(db, str(semester_id))


@router.put("/semesters/{semester_id}", response_model=SemesterResponse)
def update_semester(semester_id: UUID, payload: SemesterUpdate, db=Depends(get_db), _: dict = Depends(get_current_user)):
    return service.update_semester(db, str(semester_id), payload)


@router.delete("/semesters/{semester_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_semester(semester_id: UUID, db=Depends(get_db), _: dict = Depends(get_current_user)):
    service.delete_semester(db, str(semester_id))
    return None
