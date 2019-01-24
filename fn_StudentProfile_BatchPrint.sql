SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
ALTER FUNCTION [custom].[fn_StudentProfile_BatchPrint] (
    @schoolname VARCHAR(100)
    )
RETURNS TABLE
AS
RETURN
(
-- 'San Francisco Bay'
    SELECT
          dim.schoolname_mostrecent AS school
        , hr_info.schoolyear4digit AS schoolyear
        , dim.systemstudentid AS studentID
        , dim.GradeLevel_Numeric AS grade_numeric
        , dim.gradeLevel AS grade
        , dim.gradelevel + '_'+ hr_info.course_section + '_' + REPLACE(REPLACE(dim.fullname,',',''),' ','_') AS filename
    FROM dw.dw_dimstudent dim
    INNER JOIN dw.dw_dimschool sc 
        ON dim.schoolkey_mostrecent = sc.schoolkey
    INNER JOIN custom.vw_enrollment_course_section_ps hr_info 
        ON dim.systemstudentid = CONVERT(VARCHAR(50), CONVERT(BIGINT,hr_info.student_number))
        AND CONVERT(VARCHAR, sc.SystemSchoolID) = CONVERT(VARCHAR, hr_info.schoolid_record)
        AND hr_info.schoolyear4digit = (SELECT custom.fn_SchoolYear4Digit(GETDATE()))
    WHERE dim.systemstudentid!='-----'
        AND dim.enrollmentstatus = 'Currently Enrolled'
        AND dim.schoolname_mostrecent = @schoolname
        AND hr_info.subject = 'HR'
        AND hr_info.schoolyear4digit = (SELECT custom.fn_SchoolYear4Digit(GETDATE()))
);



GO
