from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

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

DbSession = Annotated[object, Depends(get_db)]
SkipParam = Annotated[int, Query(0, ge=0)]
LimitParam = Annotated[int, Query(50, ge=1, le=100)]
ActiveOnlyParam = Annotated[bool, Query(True)]
CampusFilterParam = Annotated[int | None, Query(None, ge=1)]
CollegeFilterParam = Annotated[int | None, Query(None, ge=1)]
ResourcesParam = Annotated[str, Query("campuses")]


@router.get("/dropdowns", response_model=dict[str, list[dict]])
def get_dropdowns(
    resources: ResourcesParam,
    campus_id: CampusFilterParam,
    college_id: CollegeFilterParam,
    skip: SkipParam,
    limit: LimitParam,
    active_only: ActiveOnlyParam,
    db: DbSession,
):
    allowed = {"campuses", "colleges", "departments", "school_years", "semesters"}
    selected = [item.strip().lower() for item in resources.split(",") if item.strip()]

    if not selected:
        raise HTTPException(status_code=400, detail="resources cannot be empty")

    invalid = [item for item in selected if item not in allowed]
    if invalid:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid resources: {', '.join(invalid)}",
        )

    data: dict[str, list[dict]] = {}

    if "campuses" in selected:
        data["campuses"] = service.list_campuses(db, skip, limit, active_only)
    if "colleges" in selected:
        data["colleges"] = service.list_colleges(db, campus_id, skip, limit, active_only)
    if "departments" in selected:
        data["departments"] = service.list_departments(db, college_id, skip, limit, active_only)
    if "school_years" in selected:
        data["school_years"] = service.list_school_years(db, skip, limit)
    if "semesters" in selected:
        data["semesters"] = service.list_semesters(db, skip, limit)

    return data


# ============================================================
# Campuses
# ============================================================


@router.post("/campuses", response_model=CampusResponse, status_code=status.HTTP_201_CREATED)
def create_campus(
    payload: CampusCreate,
    db: DbSession,
):
    return service.create_campus(db, payload)


@router.get("/campuses", response_model=list[CampusResponse])
def list_campuses(
    skip: SkipParam,
    limit: LimitParam,
    active_only: ActiveOnlyParam,
    db: DbSession,
):
    return service.list_campuses(db, skip, limit, active_only)


@router.get("/campuses/{campus_id}", response_model=CampusResponse)
def get_campus(
    campus_id: int,
    db: DbSession,
):
    return service.get_campus(db, campus_id)


@router.put("/campuses/{campus_id}", response_model=CampusResponse)
def update_campus(
    campus_id: int,
    payload: CampusUpdate,
    db: DbSession,
):
    return service.update_campus(db, campus_id, payload)


@router.delete("/campuses/{campus_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_campus(
    campus_id: int,
    db: DbSession,
):
    service.delete_campus(db, campus_id)
    return None


# ============================================================
# Colleges
# ============================================================


@router.post("/colleges", response_model=CollegeResponse, status_code=status.HTTP_201_CREATED)
def create_college(
    payload: CollegeCreate,
    db: DbSession,
):
    return service.create_college(db, payload)


@router.get("/colleges", response_model=list[CollegeResponse])
def list_colleges(
    campus_id: CampusFilterParam,
    skip: SkipParam,
    limit: LimitParam,
    active_only: ActiveOnlyParam,
    db: DbSession,
):
    return service.list_colleges(db, campus_id, skip, limit, active_only)


@router.get("/campuses/{campus_id}/colleges", response_model=list[CollegeResponse])
def list_colleges_by_campus(
    campus_id: int,
    skip: SkipParam,
    limit: LimitParam,
    active_only: ActiveOnlyParam,
    db: DbSession,
):
    return service.list_colleges(db, campus_id, skip, limit, active_only)


@router.get("/colleges/{college_id}", response_model=CollegeResponse)
def get_college(
    college_id: int,
    db: DbSession,
):
    return service.get_college(db, college_id)


@router.put("/colleges/{college_id}", response_model=CollegeResponse)
def update_college(
    college_id: int,
    payload: CollegeUpdate,
    db: DbSession,
):
    return service.update_college(db, college_id, payload)


@router.delete("/colleges/{college_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_college(
    college_id: int,
    db: DbSession,
):
    service.delete_college(db, college_id)
    return None


# ============================================================
# Departments
# ============================================================


@router.post("/departments", response_model=DepartmentResponse, status_code=status.HTTP_201_CREATED)
def create_department(
    payload: DepartmentCreate,
    db: DbSession,
):
    return service.create_department(db, payload)


@router.get("/departments", response_model=list[DepartmentResponse])
def list_departments(
    college_id: CollegeFilterParam,
    skip: SkipParam,
    limit: LimitParam,
    active_only: ActiveOnlyParam,
    db: DbSession,
):
    return service.list_departments(db, college_id, skip, limit, active_only)


@router.get("/colleges/{college_id}/departments", response_model=list[DepartmentResponse])
def list_departments_by_college(
    college_id: int,
    skip: SkipParam,
    limit: LimitParam,
    active_only: ActiveOnlyParam,
    db: DbSession,
):
    return service.list_departments(db, college_id, skip, limit, active_only)


@router.get("/departments/{department_id}", response_model=DepartmentResponse)
def get_department(
    department_id: int,
    db: DbSession,
):
    return service.get_department(db, department_id)


@router.put("/departments/{department_id}", response_model=DepartmentResponse)
def update_department(
    department_id: int,
    payload: DepartmentUpdate,
    db: DbSession,
):
    return service.update_department(db, department_id, payload)


@router.delete("/departments/{department_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_department(
    department_id: int,
    db: DbSession,
):
    service.delete_department(db, department_id)
    return None


# ============================================================
# School Years
# ============================================================


@router.post("/school-years", response_model=SchoolYearResponse, status_code=status.HTTP_201_CREATED)
def create_school_year(
    payload: SchoolYearCreate,
    db: DbSession,
):
    return service.create_school_year(db, payload)


@router.get("/school-years", response_model=list[SchoolYearResponse])
def list_school_years(
    skip: SkipParam,
    limit: LimitParam,
    db: DbSession,
):
    return service.list_school_years(db, skip, limit)


@router.get("/school-years/{school_year_id}", response_model=SchoolYearResponse)
def get_school_year(
    school_year_id: int,
    db: DbSession,
):
    return service.get_school_year(db, school_year_id)


@router.put("/school-years/{school_year_id}", response_model=SchoolYearResponse)
def update_school_year(
    school_year_id: int,
    payload: SchoolYearUpdate,
    db: DbSession,
):
    return service.update_school_year(db, school_year_id, payload)


@router.delete("/school-years/{school_year_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_school_year(
    school_year_id: int,
    db: DbSession,
):
    service.delete_school_year(db, school_year_id)
    return None


# ============================================================
# Semesters
# ============================================================


@router.post("/semesters", response_model=SemesterResponse, status_code=status.HTTP_201_CREATED)
def create_semester(
    payload: SemesterCreate,
    db: DbSession,
):
    return service.create_semester(db, payload)


@router.get("/semesters", response_model=list[SemesterResponse])
def list_semesters(
    skip: SkipParam,
    limit: LimitParam,
    db: DbSession,
):
    return service.list_semesters(db, skip, limit)


@router.get("/semesters/{semester_id}", response_model=SemesterResponse)
def get_semester(
    semester_id: int,
    db: DbSession,
):
    return service.get_semester(db, semester_id)


@router.put("/semesters/{semester_id}", response_model=SemesterResponse)
def update_semester(
    semester_id: int,
    payload: SemesterUpdate,
    db: DbSession,
):
    return service.update_semester(db, semester_id, payload)


@router.delete("/semesters/{semester_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_semester(
    semester_id: int,
    db: DbSession,
):
    service.delete_semester(db, semester_id)
    return None
