select
    af.id as "ID Actividad",
    cast(af.baselineplannedlaborunits as float) as "total_hh_actividad",
    cast(af.performancepercentcomplete as float) as activity_percentcomplete
from pxrptuser.ACTIVITY_FULL af
inner join pxrptuser.PROJECT_FULL pf on pf.objectid = af.projectobjectid
where pf.id = '{proj_name}' and af.type <> 'Finish Milestone' and  af.type <> 'Start Milestone'