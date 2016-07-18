"""
Partitionned EDF using PartitionedScheduler.
"""
from simso.core.Scheduler import SchedulerInfo
from simso.utils import PartitionedScheduler
from simso.schedulers import scheduler

@scheduler("simso.schedulers.P_RM_CUSTOM")
class P_RM(PartitionedScheduler):
    def init(self):
        PartitionedScheduler.init(
            self, SchedulerInfo("simso.schedulers.RM_mono"))

    def urm(self, n):
        return n * (2**(1.0/n) - 1)

    def packer(self):
        # First Fit
        cpus = [[cpu, 0, 0] for cpu in self.processors]

        for task in self.task_list:
            j = -1

            # Take first processor with a lower utilization than Urm(x+1)
            for i, c in enumerate(cpus):
                x = c[2]
                u = c[1] + float(task.wcet) / task.period
                if u <= self.urm(x+1):
                    j = i
                    c[2] += 1
                    break

            if j == -1:
                return False


            # Affect it to the task.
            self.affect_task_to_processor(task, cpus[j][0])

            # Update cpu.
            cpus[j][1] += float(task.wcet) / task.period
        return True
