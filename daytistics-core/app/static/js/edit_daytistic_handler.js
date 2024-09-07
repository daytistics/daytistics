function editDaytisticHandler(csrfToken) {
  return {
    addActivityResult: "",
    csrfToken: csrfToken,

    async addActivity(route) {
      try {
        const response = await fetch(route, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": this.csrfToken,
          },
          body: JSON.stringify({
            activity_id: document.querySelector('select[name="activity_id"]')
              .value,
            duration: document.querySelector('input[name="duration"]').value,
          }),
        });

        const contentType = response.headers.get("Content-Type");
        let data;

        if (contentType && contentType.includes("application/json")) {
          data = await response.json();
        } else {
          data = await response.text();
          document.querySelector("#add-activity-result").innerHTML = data;
        }
      } catch (error) {
        console.error("Error:", error);
      }
    },

    async deleteDaytistic(route) {
      deletionConfirmed = confirm(
        "Are you sure you want to delete this daytistic?"
      );

      if (!deletionConfirmed) {
        return;
      }

      try {
        await fetch(route, {
          method: "DELETE",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": this.csrfToken,
          },
        });
      } catch (error) {
        console.error("Error:", error);
      } finally {
        location.reload();
      }
    },

    async editActivity(activityEntryId, route) {
      try {
        const activityId = document.querySelector(
          `select[name="activity_${activityEntryId}"]`
        ).value;
        const duration = document.querySelector(
          `input[name="duration_${activityEntryId}"]`
        ).value;

        const shouldBeDeleted = duration === "00:00" ? true : false;

        const response = await fetch(route, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": this.csrfToken,
          },
          body: JSON.stringify({
            activityEntryId: activityEntryId,
            activityId: activityId,
            duration: duration,
            delete: shouldBeDeleted,
          }),
        });

        const contentType = response.headers.get("Content-Type");
        let data;

        if (contentType && contentType.includes("application/json")) {
          data = await response.json();
        } else {
          data = await response.text();
          document.querySelector("#edit-activities-result").innerHTML = data;
        }
      } catch (error) {
        console.error("Error:", error);
      }
    },

    async toggleImportant(route) {
      try {
        const response = await fetch(route, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": this.csrfToken,
          },
        });

        if (response.ok) {
          const data = await response.json();
          const starContainer = document.querySelector("#star-container");

        } else {
          console.error("Failed to toggle importance");
        }
      } catch (error) {
        console.error("Error:", error);
      }
    },
  };
}
