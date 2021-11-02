SELECT
      lks.SchoolName_Tableau AS SchoolName
    , cs.CurrGradeLevel
    , cs.student_number
    , cs.lastfirst
FROM custom.vw_enrollment_course_section_ps cs
LEFT JOIN custom.lkSchools lks
    ON cs.schoolid_record = lks.SystemSchoolID
    AND cs.CurrGradeLevel BETWEEN lks.LowGrade AND lks.HighGrade
WHERE cs.Schoolyear4digit = custom.fn_SchoolYear4Digit (GETDATE())
    AND cs.seq_latestEnrollment = 1
    AND cs.subject = 'HR'
    AND lks.SchoolName_Tableau = ?
ORDER BY SchoolName, cs.CurrGradeLevel, cs.lastfirst